"""
ContextIQ — Phase 10 Evaluation Framework Integration Tests
Validates benchmark dataset, Precision@k, Recall@k, MRR calculations, evaluator runs, and REST endpoints.
"""

from fastapi.testclient import TestClient

from evaluation.benchmark_dataset import BENCHMARK_TEST_CASES
from evaluation.metrics import calculate_precision_at_k, calculate_recall_at_k, calculate_reciprocal_rank
from evaluation.evaluator import BenchmarkEvaluator
from api.main import app

client = TestClient(app)


def test_benchmark_dataset_integrity():
    """Verify 30 benchmark test cases are populated with ground truth."""
    assert len(BENCHMARK_TEST_CASES) == 30
    for tc in BENCHMARK_TEST_CASES:
        assert "id" in tc
        assert "question" in tc
        assert "expected_doc_ids" in tc
        assert "category" in tc


def test_metrics_calculation_math():
    """Test Precision@k, Recall@k, and MRR calculations."""
    retrieved = ["DOC-001", "DOC-002", "DOC-003"]
    expected = ["DOC-001", "DOC-005"]

    # Precision@3 = 1 / 3 = 0.3333
    p3 = calculate_precision_at_k(retrieved, expected, k=3)
    assert p3 == 0.3333

    # Recall@3 = 1 / 2 = 0.5
    r3 = calculate_recall_at_k(retrieved, expected, k=3)
    assert r3 == 0.5

    # MRR = 1 / 1 = 1.0 (DOC-001 is first)
    mrr = calculate_reciprocal_rank(retrieved, expected)
    assert mrr == 1.0


def test_evaluator_sample_run():
    """Test BenchmarkEvaluator runs over sample test cases."""
    evaluator = BenchmarkEvaluator()
    summary = evaluator.evaluate_all(limit=2)

    assert summary["total_benchmark_cases"] == 2
    assert "precision_at_3" in summary
    assert "recall_at_3" in summary
    assert "mean_reciprocal_rank" in summary
    assert "mean_groundedness_score" in summary


def test_evaluation_api_endpoints():
    """Test GET /api/v1/evaluation/metrics and GET /api/v1/evaluation/test-cases."""
    res_m = client.get("/api/v1/evaluation/metrics")
    assert res_m.status_code == 200
    data_m = res_m.json()
    assert "precision_at_3" in data_m
    assert "recall_at_3" in data_m
    assert "mean_reciprocal_rank" in data_m

    res_tc = client.get("/api/v1/evaluation/test-cases")
    assert res_tc.status_code == 200
    data_tc = res_tc.json()
    assert len(data_tc) == 30
