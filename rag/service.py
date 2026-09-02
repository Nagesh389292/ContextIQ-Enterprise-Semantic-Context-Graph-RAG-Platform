"""
ContextIQ — Grounded RAG Master Service (Gemini 2.0 Flash Integration)
Orchestrates hybrid retrieval, Gemini 2.0 Flash prompt generation, citation grounding, and SSE trace streaming.
"""

from typing import Dict, Any, List, Optional, AsyncGenerator
import json
import asyncio
from loguru import logger

from config import settings
from retrieval.hybrid_pipeline import get_hybrid_pipeline
from rag.prompt_builder import PromptBuilder
from rag.grounding_validator import GroundingValidator

_rag_service_instance: Optional["RAGService"] = None


class RAGService:
    """Master Grounded RAG Generation Service."""

    def __init__(self):
        self.hybrid_pipeline = get_hybrid_pipeline()
        self.prompt_builder = PromptBuilder()
        self.validator = GroundingValidator()
        self._genai_client = None

    def _get_genai_client(self):
        """Lazy load google-genai client if API key is present."""
        if self._genai_client is None and settings.is_llm_available:
            try:
                from google import genai
                self._genai_client = genai.Client(api_key=settings.gemini_api_key)
                logger.info(f"Initialized Google GenAI client (model: {settings.gemini_model}).")
            except Exception as exc:
                logger.warning(f"Could not initialize Google GenAI client: {exc}")
        return self._genai_client

    def generate_grounded_answer(
        self,
        question: str,
        top_k: int = 5,
        plant_id: Optional[str] = None,
        doc_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute full RAG generation pipeline: Retrieval -> RRF Rerank -> Prompt Assembly -> LLM -> Grounding Audit."""
        # 1. Execute Hybrid Search & Graph Context Expansion
        retrieval_bundle = self.hybrid_pipeline.search(
            query=question, top_k=top_k, plant_id=plant_id, doc_type=doc_type, expand_graph=True
        )

        top_chunks = retrieval_bundle.get("top_chunks", [])
        graph_context = retrieval_bundle.get("graph_context", {})

        # 2. Build Grounded Prompt
        prompt_text = self.prompt_builder.build_prompt(query=question, context_bundle=retrieval_bundle)

        # 3. LLM Generation (Gemini 2.0 Flash or Grounded Fallback Synthesizer)
        client = self._get_genai_client()
        raw_answer = ""
        model_used = settings.gemini_model

        if client is not None:
            try:
                response = client.models.generate_content(
                    model=settings.gemini_model,
                    contents=prompt_text,
                )
                raw_answer = response.text.strip()
            except Exception as exc:
                logger.warning(f"Gemini API generation failed ({exc}). Using deterministic grounded synthesizer.")
                raw_answer = self._synthesize_grounded_answer(question, top_chunks, graph_context)
                model_used = f"{settings.gemini_model} (Grounded Synthesizer Fallback)"
        else:
            raw_answer = self._synthesize_grounded_answer(question, top_chunks, graph_context)
            model_used = "ContextIQ Grounded Synthesizer (Demo Engine)"

        # 4. Validate Grounding & Citations
        validation = self.validator.validate(answer=raw_answer, context_bundle=retrieval_bundle)

        # 5. Extract Citations & Evidence
        citations = []
        for chunk in top_chunks:
            cid = chunk.get("chunk_id")
            if cid in validation.get("valid_chunk_citations", []) or cid in validation.get("chunk_citations_found", []):
                citations.append({
                    "citation_id": f"[{cid}]",
                    "chunk_id": cid,
                    "document_id": chunk.get("document_id"),
                    "document_title": chunk.get("document_title"),
                    "section": chunk.get("section"),
                    "snippet": chunk.get("text", "")[:180],
                    "matched_sources": chunk.get("matched_sources", []),
                    "score": chunk.get("rrf_score", 0.0),
                })

        return {
            "question": question,
            "answer": raw_answer,
            "model": model_used,
            "grounding_score": validation["grounding_score"],
            "is_grounded": validation["is_grounded"],
            "citations_count": len(citations),
            "citations": citations,
            "retrieved_chunks_count": len(top_chunks),
            "entities_extracted": retrieval_bundle.get("entities_found", []),
            "graph_triples_expanded": graph_context.get("triples_count", 0),
            "retrieval_metadata": retrieval_bundle.get("retrieval_metadata", {}),
            "execution_trace": [
                {"step": 1, "name": "Hybrid Candidate Retrieval", "details": "Retrieved candidate chunks via BM25 & ChromaDB vector store."},
                {"step": 2, "name": "Reciprocal Rank Fusion", "details": "Fused top candidate ranks using RRF (k=60)."},
                {"step": 3, "name": "Cypher Graph Expansion", "details": "Expanded 2-hop graph neighborhood in Neo4j."},
                {"step": 4, "name": "Grounded LLM Generation", "details": f"Generated response using {model_used}."},
                {"step": 5, "name": "Faithfulness & Grounding Audit", "details": f"Grounding Score: {validation['grounding_score']} (Citations: {len(citations)})."}
            ]
        }

    def _synthesize_grounded_answer(
        self, question: str, top_chunks: List[Dict[str, Any]], graph_context: Dict[str, Any]
    ) -> str:
        """Deterministic grounded synthesizer formatting response when Gemini API key is absent."""
        if not top_chunks:
            return "Information not available in enterprise context."

        q_lower = question.lower()
        # Unsupported domain query check (e.g. HR, Vacation, Payroll, Marketing)
        unsupported_keywords = ["vacation", "marketing", "payroll", "salary", "bonus", "leave policy", "hiring"]
        if any(kw in q_lower for kw in unsupported_keywords):
            return "Information not available in enterprise context."

        c1 = top_chunks[0]
        cid = c1.get("chunk_id", "DOC-001_CHUNK_01")
        doc_title = c1.get("document_title", "Manual")
        section = c1.get("section", "General")
        text = c1.get("text", "")
        plant = c1.get("metadata", {}).get("plant_id", "P001")
        machine = c1.get("metadata", {}).get("machine_id", "M001")

        lines = [
            f"Based on enterprise documentation [{cid}], the operational directive for **{doc_title}** ({section}) specifies:",
            f"",
            f"> \"{text[:260]}...\"",
            f"",
            f"### Key Operational Parameters & Guardrails",
            f"- **Facility Context**: Plant [{plant}] ({c1.get('metadata', {}).get('process', 'Operations')})",
            f"- **Asset ID**: Machine [{machine}]",
            f"- **Source Reference**: Standard Operating Procedure [{cid}]",
            f"",
            f"### Grounded Citations",
            f"- Document Citation: [{cid}] ({doc_title})",
            f"- Entity References: [Machine:{machine}], [Plant:{plant}]"
        ]
        return "\n".join(lines)

    async def stream_rag_trace(self, question: str) -> AsyncGenerator[str, None]:
        """SSE streaming generator yielding step-by-step execution trace events and answer chunks."""
        # Step 1: Retrieval
        yield f"data: {json.dumps({'event': 'trace', 'step': 'RETRIEVAL', 'message': 'Executing BM25 + Vector Search'})}\n\n"
        await asyncio.sleep(0.1)

        result = self.generate_grounded_answer(question=question)

        chunks_cnt = result["retrieved_chunks_count"]
        triples_cnt = result["graph_triples_expanded"]

        # Step 2: RRF Rerank
        yield f"data: {json.dumps({'event': 'trace', 'step': 'RRF_FUSION', 'message': f'Reranked top {chunks_cnt} chunks via Reciprocal Rank Fusion'})}\n\n"
        await asyncio.sleep(0.1)

        # Step 3: Graph Expansion
        yield f"data: {json.dumps({'event': 'trace', 'step': 'GRAPH_EXPANSION', 'message': f'Expanded {triples_cnt} 2-hop Cypher triples'})}\n\n"
        await asyncio.sleep(0.1)

        # Step 4: Answer Generation Payload
        yield f"data: {json.dumps({'event': 'answer', 'data': result})}\n\n"
        yield f"data: [DONE]\n\n"


def get_rag_service() -> RAGService:
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance
