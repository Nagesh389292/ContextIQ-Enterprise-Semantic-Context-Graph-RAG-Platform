"""
ContextIQ — Phase Q Regression Test Suite
Validates Query Understanding Layer, Domain Intent Routing, Document Diversity, and Regression Scenarios.
"""

import pytest
from retrieval.query_understanding import get_query_engine, QueryAnalysis
from retrieval.hybrid_pipeline import get_hybrid_pipeline

query_engine = get_query_engine()
pipeline = get_hybrid_pipeline()


class TestPhaseQQueryUnderstanding:

    def test_maintenance_intent_classification(self):
        analysis = query_engine.analyze("What maintenance procedure applies to machine M001?")
        assert analysis.intent == "maintenance"
        assert "M001" in analysis.entities
        assert analysis.confidence >= 0.8

    def test_supplier_intent_classification(self):
        analysis = query_engine.analyze("What SLA terms apply to Tier 1 supplier S001 for spare parts?")
        assert analysis.intent == "supplier"
        assert "S001" in analysis.entities

    def test_production_intent_classification(self):
        analysis = query_engine.analyze("What is the operation manual for welding robot M008 at Plant P003?")
        assert analysis.intent == "production"
        assert "M008" in analysis.entities
        assert "P003" in analysis.entities

    def test_quality_intent_classification(self):
        analysis = query_engine.analyze("What SPC Cpk threshold requires process stoppage at Plant P001?")
        assert analysis.intent == "quality"
        assert "P001" in analysis.entities

    def test_unsupported_edgecase_classification(self):
        analysis = query_engine.analyze("What is the vacation policy for employees in Marketing?")
        assert analysis.intent == "unsupported"
        assert analysis.confidence >= 0.90


class TestPhaseQRetrievalRegression:

    def test_unsupported_query_returns_empty(self):
        result = pipeline.search("What is the vacation policy for employees in Marketing?", top_k=5)
        assert result["total_retrieved_chunks"] == 0
        assert result["top_chunks"] == []

    def test_maintenance_query_execution(self):
        result = pipeline.search("What maintenance procedure applies to machine M001?", top_k=5)
        assert result["total_retrieved_chunks"] > 0
        doc_ids = [c["document_id"] for c in result["top_chunks"]]
        assert len(set(doc_ids)) > 1  # Document diversity verified

    def test_supplier_query_execution(self):
        result = pipeline.search("Which supplier and material information is associated with replacement parts for M001?", top_k=5)
        assert result["total_retrieved_chunks"] > 0

    def test_quality_query_execution(self):
        result = pipeline.search("How are non-conforming parts quarantined during batch inspection at P002?", top_k=5)
        assert result["total_retrieved_chunks"] > 0
