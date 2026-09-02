"""
ContextIQ — Phase S Regression Test Suite
Validates Config G vs H Parity, Relevance-Aware Diversity Filtering, and Domain Ranking.
"""

import pytest
from retrieval.reranker import RRFReranker
from retrieval.hybrid_pipeline import get_hybrid_pipeline

reranker = RRFReranker()
pipeline = get_hybrid_pipeline()


class TestPhaseSRelevanceAwareDiversity:

    def test_relevance_aware_diversity_preserves_high_scoring_chunks(self):
        chunks = [
            {"chunk_id": "C1", "document_id": "DOC-001", "section": "Sec 1", "rrf_score": 0.95},
            {"chunk_id": "C2", "document_id": "DOC-001", "section": "Sec 2", "rrf_score": 0.88},
            {"chunk_id": "C3", "document_id": "DOC-001", "section": "Sec 3", "rrf_score": 0.75},
            {"chunk_id": "C4", "document_id": "DOC-002", "section": "Sec 1", "rrf_score": 0.40},
            {"chunk_id": "C5", "document_id": "DOC-003", "section": "Sec 1", "rrf_score": 0.30},
        ]
        result = reranker.apply_relevance_aware_diversity(chunks, top_k=5)
        # Highly relevant chunks (scores >= 0.45) from DOC-001 are preserved rather than rigidly capped at 2
        assert len(result) == 5
        doc1_chunks = [c for c in result if c["document_id"] == "DOC-001"]
        assert len(doc1_chunks) == 3


class TestPhaseSConfigHParity:

    def test_hybrid_pipeline_preserves_high_recall(self):
        res = pipeline.search("What maintenance procedure applies to machine M001?", top_k=5)
        assert res["total_retrieved_chunks"] > 0
        top_docs = [c["document_id"] for c in res["top_chunks"]]
        assert "DOC-031" in top_docs or "DOC-028" in top_docs

    def test_supplier_contract_relationship_retrieval(self):
        res = pipeline.search("Which supplier SLA applies to replacement bearing B101 for MAT-001?", top_k=5)
        assert res["total_retrieved_chunks"] > 0
        top_docs = [c["document_id"] for c in res["top_chunks"]]
        assert "DOC-006" in top_docs or "DOC-024" in top_docs
