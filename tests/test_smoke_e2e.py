"""
ContextIQ — End-to-End API Smoke Test Suite
Tests live FastAPI routes (/health, /ready, /graph, /documents, /search, /rag, /agent, /governance, /evaluation)
using Starlette TestClient without artificial mocks.
"""

from fastapi.testclient import TestClient
import pytest

from api.main import app

client = TestClient(app)


class TestProductionSmokeSuite:
    """End-to-end smoke test suite executing against real API endpoints."""

    def test_health_liveness_probe(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data

    def test_readiness_probe(self):
        response = client.get("/api/v1/ready")
        assert response.status_code == 200
        data = response.json()
        assert "is_ready" in data
        assert "dependencies" in data
        assert "chromadb" in data["dependencies"]

    def test_graph_stats_api(self):
        response = client.get("/api/v1/graph/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_nodes" in data or "node_count" in data or "status" in data

    def test_document_list_api(self):
        response = client.get("/api/v1/documents")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_hybrid_search_api(self):
        response = client.post("/api/v1/search/hybrid", json={"query": "machine maintenance", "top_k": 3})
        assert response.status_code == 200
        data = response.json()
        assert "top_chunks" in data or "fused_results" in data or "results" in data

    def test_rag_generation_api(self):
        response = client.post("/api/v1/rag/query", json={"question": "What maintenance procedure applies to machine M001?"})
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "citations" in data

    def test_agent_query_api(self):
        response = client.post("/api/v1/agent/query", json={"question": "Check status of machine M001"})
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "execution_trace" in data

    def test_governance_shacl_report_api(self):
        response = client.get("/api/v1/governance/shacl-report")
        assert response.status_code == 200
        data = response.json()
        assert "compliance_score" in data or "conforms" in data or "semantic_validity_score" in data

    def test_evaluation_metrics_api(self):
        response = client.get("/api/v1/evaluation/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "precision_at_3" in data or "mrr" in data
