"""
ContextIQ — Evaluation API Routes
Exposes GET /api/v1/evaluation/metrics, GET /api/v1/evaluation/test-cases, and POST /api/v1/evaluation/run.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query

from evaluation.evaluator import get_evaluator, BenchmarkEvaluator
from evaluation.benchmark_dataset import BENCHMARK_TEST_CASES

router = APIRouter(prefix="", tags=["Evaluation Framework"])


@router.get("/metrics")
def get_evaluation_metrics(
    evaluator: BenchmarkEvaluator = Depends(get_evaluator)
):
    """Retrieve system-wide Precision@k, Recall@k, MRR, and Groundedness benchmark metrics."""
    metrics = evaluator.evaluate_all(limit=None)
    return {
        "total_test_cases": metrics.get("total_benchmark_cases", len(BENCHMARK_TEST_CASES)),
        "precision_at_1": metrics.get("precision_at_1", 0.0),
        "precision_at_3": metrics.get("precision_at_3", 0.0),
        "precision_at_5": metrics.get("precision_at_5", 0.0),
        "recall_at_1": metrics.get("recall_at_1", 0.0),
        "recall_at_3": metrics.get("recall_at_3", 0.0),
        "recall_at_5": metrics.get("recall_at_5", 0.0),
        "mean_reciprocal_rank": metrics.get("mean_reciprocal_rank", 0.0),
        "mean_groundedness_score": metrics.get("mean_groundedness_score", 0.0),
        "groundedness_pass_rate": metrics.get("groundedness_pass_rate", 0.0),
    }


@router.get("/test-cases")
def get_evaluation_test_cases():
    """Retrieve 30 benchmark ground-truth test cases."""
    return BENCHMARK_TEST_CASES


@router.post("/run")
def run_evaluation_benchmark(
    limit: Optional[int] = Query(default=None, description="Optional limit of test cases to run"),
    evaluator: BenchmarkEvaluator = Depends(get_evaluator)
):
    """Trigger a full benchmark evaluation run over the 30 test cases."""
    summary = evaluator.evaluate_all(limit=limit)
    return summary
