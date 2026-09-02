"""
ContextIQ — Master Hybrid Search & Retrieval Pipeline
Coordinates BM25 Lexical search, ChromaDB Vector search, RRF Reranking, and Graph Context Expansion.
"""

from typing import Dict, Any, List, Optional
from loguru import logger

from retrieval.lexical import BM25LexicalRetriever
from retrieval.vector import VectorRetriever
from retrieval.reranker import RRFReranker
from retrieval.graph_expander import GraphContextExpander
from retrieval.models import HybridRetrievalResult, RetrievedChunk, GraphSubContext
from documents.entity_linking.graph_linker import GraphLinker

_pipeline_instance: Optional["HybridSearchPipeline"] = None


from retrieval.query_understanding import get_query_engine
from retrieval.relational_candidates import get_relational_generator
from retrieval.evidence import (
    EvidenceBundle, DocumentEvidence, EntityEvidence, RelationshipEvidence, GraphEvidence
)


class HybridSearchPipeline:
    """Unified hybrid retrieval pipeline combining Lexical + Vector + Relational Graph + Evidence Diversity."""

    def __init__(self):
        self.lexical_retriever = BM25LexicalRetriever()
        self.vector_retriever = VectorRetriever()
        self.reranker = RRFReranker()
        self.graph_expander = GraphContextExpander()
        self.relational_generator = get_relational_generator()
        self.entity_linker = GraphLinker()
        self.query_engine = get_query_engine()

    def search(
        self,
        query: str,
        top_k: int = 5,
        plant_id: Optional[str] = None,
        doc_type: Optional[str] = None,
        expand_graph: bool = True
    ) -> Dict[str, Any]:
        """Execute relationship-first hybrid search over enterprise corpus and knowledge graph."""
        query_analysis = self.query_engine.analyze(query)
        query_entity_ids = query_analysis.entities
        query_intent = query_analysis.intent

        if query_intent == "unsupported":
            return EvidenceBundle(
                query=query, intent=query_intent, total_retrieved=0, provenance={"query_intent": "unsupported"}
            ).to_dict()

        where_filter = {}
        if plant_id:
            where_filter["plant_id"] = plant_id
        if doc_type:
            where_filter["document_type"] = doc_type

        # 1. Intent-Driven Relational Candidate Generation & Multi-Hop Graph Traversal
        relational_candidates = self.relational_generator.get_relational_candidates(
            intent=query_intent,
            entity_ids=query_entity_ids,
            max_hops=3,
            max_candidates=10
        )
        graph_target_docs = list(dict.fromkeys([c["document_id"] for c in relational_candidates]))
        rel_evidences, legacy_graph_docs = self.graph_expander.plan_and_traverse(query_intent, query_entity_ids)
        graph_target_docs = list(dict.fromkeys(graph_target_docs + legacy_graph_docs))

        expanded_query = query
        if query_entity_ids:
            expanded_query = f"{query} {' '.join(query_entity_ids)}"

        # 2. Parallel Candidate Generation (BM25 + Vector + Relational Graph Candidates)
        # AE-2 (Phase AE) — candidate pool floor raised from 20 → 30.
        # Expanding the BM25+vector fetch window recovers documents ranked 21–30
        # that were previously invisible to the reranker (validated offline:
        # pool=30 was the sole AE variant to pass all 5 acceptance gate metrics).
        candidate_k = max(top_k * 4, 30)
        vector_candidates = self.vector_retriever.search(
            query=expanded_query, top_k=candidate_k, where_filter=where_filter if where_filter else None
        )
        bm25_candidates = self.lexical_retriever.search(
            query=expanded_query, top_k=candidate_k, where_filter=where_filter if where_filter else None
        )

        # 3. Multi-Feature Relationship Join Reranking & Evidence Diversity
        reranked_chunks = self.reranker.rerank(
            bm25_results=bm25_candidates,
            vector_results=vector_candidates,
            entity_results=relational_candidates,
            graph_target_doc_ids=graph_target_docs,
            query_intent=query_intent,
            query_entities=query_entity_ids,
            top_k=top_k,
            apply_diversity=True
        )

        # 4. Convert Chunks into DocumentEvidence Objects
        doc_evidences = []
        for c in reranked_chunks:
            doc_evidences.append(DocumentEvidence(
                chunk_id=c.get("chunk_id", ""),
                document_id=c.get("document_id", ""),
                document_title=c.get("document_title", ""),
                section=c.get("section", ""),
                text=c.get("text", ""),
                score=c.get("score", 0.0),
                matched_sources=c.get("matched_sources", []),
                metadata=c.get("metadata", {})
            ))

        # 5. Extract Entities & Graph Subgraph
        extracted_entities = self.entity_linker.extract_entities(text=query, metadata={})
        for chunk in reranked_chunks:
            extracted_entities.extend(self.entity_linker.extract_entities(text=chunk.get("text", ""), metadata=chunk.get("metadata", {})))

        unique_entity_ids = list(set(e["canonical_id"] for e in extracted_entities))

        graph_context = {}
        if expand_graph and unique_entity_ids:
            graph_context = self.graph_expander.expand_entities(unique_entity_ids[:5], intent=query_intent)

        graph_evidence = GraphEvidence(
            expanded_entities=graph_context.get("entities_expanded", []),
            triples_count=graph_context.get("triples_count", 0),
            relationships=rel_evidences
        )

        bundle = EvidenceBundle(
            query=query,
            intent=query_intent,
            document_evidence=doc_evidences,
            entity_evidence=[EntityEvidence(canonical_id=e, entity_type="DomainEntity", raw_id=e, ontology_uri=f"http://example.org/ont#{e}") for e in unique_entity_ids],
            relationship_evidence=rel_evidences,
            graph_evidence=graph_evidence,
            total_retrieved=len(doc_evidences),
            provenance={
                "vector_candidates_count": len(vector_candidates),
                "bm25_candidates_count": len(bm25_candidates),
                "relational_candidates_count": len(relational_candidates),
                "relationship_targets": graph_target_docs,
                "retrieved_chunk_ids": [d.chunk_id for d in doc_evidences]
            }
        )

        return bundle.to_dict()


def get_hybrid_pipeline() -> HybridSearchPipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = HybridSearchPipeline()
    return _pipeline_instance
