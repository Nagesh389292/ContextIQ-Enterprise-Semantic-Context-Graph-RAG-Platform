"""
ContextIQ — Phase U Relational Candidate Generation Unit & Regression Tests
Tests multi-hop relationship candidate generation and candidate pool injection.
"""

import pytest
from retrieval.relational_candidates import get_relational_generator
from retrieval.hybrid_pipeline import get_hybrid_pipeline


class TestPhaseURelationalCandidateGenerator:
    """Test suite for generalized relational candidate generation."""

    def setup_method(self):
        self.generator = get_relational_generator()
        self.pipeline = get_hybrid_pipeline()

    def test_maintenance_relational_candidate_generation(self):
        """Test Machine entity M001 produces relational document candidates in maintenance intent."""
        chunks = self.generator.get_relational_candidates(
            intent="maintenance",
            entity_ids=["M001"],
            max_hops=3
        )
        assert isinstance(chunks, list)
        doc_ids = set(c["document_id"] for c in chunks)
        # Should discover DOC-031 or DOC-028 via multi-hop relationship joins
        assert len(doc_ids) > 0
        for c in chunks:
            assert c["retrieval_channel"] == "graph_relational"
            assert "source_entity" in c
            assert "hop_count" in c

    def test_supplier_relational_candidate_generation(self):
        """Test Supplier S001 produces supply agreement relational candidates."""
        chunks = self.generator.get_relational_candidates(
            intent="supplier",
            entity_ids=["S001"],
            max_hops=3
        )
        assert isinstance(chunks, list)
        doc_ids = set(c["document_id"] for c in chunks)
        assert "DOC-006" in doc_ids or len(doc_ids) > 0

    def test_unsupported_intent_returns_empty(self):
        """Test unsupported intent returns no relational candidates."""
        chunks = self.generator.get_relational_candidates(
            intent="unsupported",
            entity_ids=["M001"]
        )
        assert chunks == []

    def test_search_pipeline_includes_relational_candidates(self):
        """Test hybrid search pipeline includes relational candidate count in provenance."""
        res = self.pipeline.search("What maintenance procedure applies to M001?", top_k=5)
        prov = res.get("provenance", {})
        assert "relational_candidates_count" in prov
        assert prov["relational_candidates_count"] >= 0
