"""
ContextIQ — Grounded RAG Prompt Orchestrator
Builds grounded system prompts and context blocks enforcing explicit citations and anti-hallucination guardrails.
"""

from typing import Dict, Any, List


SYSTEM_PROMPT = """You are ContextIQ AI Copilot, an enterprise semantic context engine powering industrial operations.
Your answers MUST be strictly grounded in the provided RAG Context Bundle below.

CRITICAL RULES:
1. ONLY use factual information present in the RAG Context Bundle (Document Chunks and Knowledge Graph Triples).
2. Every major factual claim or threshold statement MUST include inline citations to its source:
   - For document chunks, cite using: [DOC-XXX_CHUNK_YY] (e.g. [DOC-001_CHUNK_01])
   - For knowledge graph entities/triples, cite using: [Entity:ID] (e.g. [Machine:M001], [Plant:P001])
3. If the context DOES NOT contain sufficient information to answer the user's question, explicitly state: "Information not available in enterprise context." DO NOT fabricate or guess facts outside the context.
4. Structure your response clearly using Markdown headings, bullet points, and an explicit **Grounded Citations** summary section at the end.
"""


class PromptBuilder:
    """Orchestrates system and context prompts for Gemini RAG generation."""

    def build_prompt(self, query: str, context_bundle: Dict[str, Any]) -> str:
        """Format full grounded prompt text containing document chunks and graph triples."""
        top_chunks: List[Dict[str, Any]] = context_bundle.get("top_chunks", [])
        graph_context: Dict[str, Any] = context_bundle.get("graph_context", {})

        # 1. Format Document Chunks Section
        chunks_text_list = []
        for idx, chunk in enumerate(top_chunks, start=1):
            cid = chunk.get("chunk_id", f"CHUNK_{idx}")
            doc_title = chunk.get("document_title", "Document")
            section = chunk.get("section", "General")
            text = chunk.get("text", "").strip()
            meta = chunk.get("metadata", {})
            plant = meta.get("plant_id", "")
            process = meta.get("process", "")

            chunks_text_list.append(
                f"--- DOCUMENT CHUNK [{cid}] ---\n"
                f"Title: {doc_title} | Section: {section}\n"
                f"Plant: {plant} | Process: {process}\n"
                f"Content:\n{text}\n"
            )

        context_chunks_str = "\n".join(chunks_text_list) if chunks_text_list else "No document chunks retrieved."

        # 2. Format Knowledge Graph Triples Section
        triples_str = "No knowledge graph triples expanded."
        if graph_context and "subgraph" in graph_context:
            subgraph = graph_context.get("subgraph", {})
            nodes = subgraph.get("nodes", [])
            relationships = subgraph.get("relationships", [])

            if nodes or relationships:
                triples_lines = []
                for node in nodes[:15]:
                    n_id = node.get("properties", {}).get("machine_id") or node.get("properties", {}).get("plant_id") or node.get("id")
                    labels = ":".join(node.get("labels", []))
                    triples_lines.append(f"Node [{labels}:{n_id}] Properties: {node.get('properties')}")

                for rel in relationships[:15]:
                    triples_lines.append(f"Relationship ({rel.get('start_node')}) -[:{rel.get('type')}]-> ({rel.get('end_node')})")

                triples_str = "\n".join(triples_lines)

        # 3. Assemble Full Prompt
        full_prompt = f"""{SYSTEM_PROMPT}

=== RAG CONTEXT BUNDLE ===

--- RETRIEVED DOCUMENT CHUNKS ---
{context_chunks_str}

--- KNOWLEDGE GRAPH SUBGRAPH ---
{triples_str}

=== USER QUESTION ===
{query}

=== GROUNDED ANSWER ===
"""
        return full_prompt
