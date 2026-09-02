"""
ContextIQ — Phase R Regression Test Suite
Validates Typed Evidence Modeling, Intent-Driven Graph Planning, Relationship-First Retrieval, and Provenance.
"""

import pytest
from retrieval.evidence import EvidenceBundle, DocumentEvidence, RelationshipEvidence
from retrieval.graph_expander import GraphContextExpander
from retrieval.hybrid_pipeline import get_hybrid_pipeline

graph_expander = GraphContextExpander()
pipeline = get_hybrid_pipeline()


class TestPhaseREvidenceModel:

    def test_evidence_bundle_serialization(self):
        bundle = EvidenceBundle(
            query="What supplier is associated with M001?",
            intent="supplier",
            document_evidence=[
                DocumentEvidence(
                    chunk_id="DOC-006_chunk_1",
                    document_id="DOC-006",
                    document_title="Supplier SLA",
                    section="Sec 1",
                    text="Supplier S001 provides MAT-001.",
                    score=0.92,
                    matched_sources=["bm25", "vector"]
                )
            ],
            relationship_evidence=[
                RelationshipEvidence(
                    subject_id="M001", subject_type="Machine",
                    predicate="SUPPLIED_BY", object_id="S001", object_type="Supplier",
                    supporting_doc_id="DOC-006"
                )
            ]
        )
        res = bundle.to_dict()
        assert res["query"] == "What supplier is associated with M001?"
        assert res["intent"] == "supplier"
        assert len(res["top_chunks"]) == 1
        assert res["top_chunks"][0]["document_id"] == "DOC-006"
        assert len(res["relationships"]) == 1
        assert res["relationships"][0]["predicate"] == "SUPPLIED_BY"


class TestPhaseRGraphRelationshipPlanning:

    def test_supplier_intent_graph_traversal(self):
        rels, target_docs = graph_expander.plan_and_traverse(intent="supplier", entities=["M001", "MAT-001"])
        assert len(rels) >= 2
        assert "DOC-006" in target_docs
        predicates = [r.predicate for r in rels]
        assert "SUPPLIED_BY" in predicates

    def test_maintenance_intent_graph_traversal(self):
        rels, target_docs = graph_expander.plan_and_traverse(intent="maintenance", entities=["M001"])
        assert len(rels) >= 2
        assert "DOC-031" in target_docs or "DOC-028" in target_docs
        predicates = [r.predicate for r in rels]
        assert "DOCUMENTED_IN_PROCEDURE" in predicates or "HAS_TECHNICAL_MANUAL" in predicates


class TestPhaseRRelationshipRetrievalRegression:

    def test_m001_to_maintenance_procedure_relationship(self):
        result = pipeline.search("What maintenance procedure applies to machine M001?", top_k=5)
        assert result["total_retrieved_chunks"] > 0
        assert "DOC-031" in [c["document_id"] for c in result["top_chunks"]] or "DOC-028" in [c["document_id"] for c in result["top_chunks"]]

    def test_mat001_to_supplier_relationship(self):
        result = pipeline.search("Which supplier SLA applies to replacement bearing B101 for MAT-001?", top_k=5)
        assert result["total_retrieved_chunks"] > 0
        top_docs = [c["document_id"] for c in result["top_chunks"]]
        assert "DOC-006" in top_docs or "DOC-024" in top_docs

    def test_po00102_to_production_relationship(self):
        result = pipeline.search("Which production order is assigned to cell RC-01 for high-precision shafts?", top_k=5)
        assert result["total_retrieved_chunks"] > 0

    def test_quality_event_to_machine_relationship(self):
        result = pipeline.search("What SPC Cpk threshold requires process stoppage at Plant P001?", top_k=5)
        assert result["total_retrieved_chunks"] > 0
