"""
Phase 6 tests — Hybrid Search, RRF Reranking, and Graph Context Expansion.
"""

import pytest
from fastapi.testclient import TestClient

from retrieval.lexical import BM25LexicalRetriever
from retrieval.vector import VectorRetriever
from retrieval.reranker import RRFReranker
from retrieval.graph_expander import GraphContextExpander
from retrieval.hybrid_pipeline import HybridSearchPipeline
from api.main import app

client = TestClient(app)


class TestBM25LexicalRetriever:

    def test_bm25_search_results(self):
        retriever = BM25LexicalRetriever()
        results = retriever.search("bearing inspection lubricant M001", top_k=3)
        assert isinstance(results, list)
        if results:
            assert "chunk_id" in results[0]
            assert "score" in results[0]
            assert results[0]["retrieval_source"] == "bm25_lexical"


class TestRRFReranker:

    def test_rrf_scoring_and_fusion(self):
        reranker = RRFReranker(k=60)
        vector_res = [
            {"chunk_id": "C01", "text": "CNC Machine M001 Overview", "metadata": {"plant_id": "P001"}},
            {"chunk_id": "C02", "text": "Bearing SOP M001", "metadata": {"plant_id": "P001"}},
        ]
        lexical_res = [
            {"chunk_id": "C02", "text": "Bearing SOP M001", "metadata": {"plant_id": "P001"}},
            {"chunk_id": "C03", "text": "Supplier Quality S001", "metadata": {"plant_id": "P002"}},
        ]

        reranked = reranker.rerank(bm25_results=lexical_res, vector_results=vector_res, top_k=3)
        assert len(reranked) == 3
        # C02 appears in both vector (rank 2) and lexical (rank 1), so it should rank highest in RRF score
        assert reranked[0]["chunk_id"] == "C02"
        assert "vector" in reranked[0]["matched_sources"]
        assert any(s in reranked[0]["matched_sources"] for s in ["lexical", "bm25"])


class TestGraphContextExpander:

    def test_expand_entities(self):
        expander = GraphContextExpander()
        res = expander.expand_entities(["M001", "P001"])
        assert "entities_expanded" in res
        assert "subgraph" in res
        assert "nodes" in res["subgraph"]


class TestHybridPipelineAndAPIs:

    def test_hybrid_pipeline_search(self):
        pipeline = HybridSearchPipeline()
        res = pipeline.search(query="bearing temperature threshold M001", top_k=3)
        assert res["query"] == "bearing temperature threshold M001"
        assert "top_chunks" in res
        assert "retrieval_metadata" in res

    def test_get_search_endpoint(self):
        res = client.get("/api/v1/search?q=bearing+overheating&top_k=3")
        assert res.status_code == 200
        data = res.json()
        assert "top_chunks" in data
        assert "retrieval_metadata" in data

    def test_post_search_hybrid_endpoint(self):
        res = client.post(
            "/api/v1/search/hybrid",
            json={"query": "hydraulic press safety P002", "top_k": 3, "plant_id": "P002"}
        )
        assert res.status_code == 200
        data = res.json()
        assert "top_chunks" in data
