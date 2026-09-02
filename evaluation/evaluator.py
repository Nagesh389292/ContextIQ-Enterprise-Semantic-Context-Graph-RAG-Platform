"""
ContextIQ — Master Benchmark Evaluator
Runs 30 ground-truth enterprise test cases through hybrid retrieval & RAG service, computing system-wide precision, recall, MRR, and groundedness metrics.
"""

from typing import Dict, Any, List, Optional
from loguru import logger

from evaluation.benchmark_dataset import BENCHMARK_TEST_CASES
from evaluation.metrics import calculate_precision_at_k, calculate_recall_at_k, calculate_reciprocal_rank
from retrieval.hybrid_pipeline import get_hybrid_pipeline
from rag.service import get_rag_service

_evaluator_instance: Optional["BenchmarkEvaluator"] = None


class BenchmarkEvaluator:
    """Master evaluator running offline & online retrieval benchmarks."""

    def __init__(self):
        self.hybrid_pipeline = get_hybrid_pipeline()
        self.rag_service = get_rag_service()

    def evaluate_all(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Run all benchmark test cases and compute aggregate precision, recall, MRR, and groundedness."""
        test_cases = BENCHMARK_TEST_CASES[:limit] if limit else BENCHMARK_TEST_CASES

        results = []
        p1_list, p3_list, p5_list = [], [], []
        r1_list, r3_list, r5_list = [], [], []
        mrr_list = []
        groundedness_list = []

        for tc in test_cases:
            tc_id = tc["id"]
            question = tc["question"]
            expected_doc_ids = tc["expected_doc_ids"]

            # 1. Execute RAG Service query
            rag_res = self.rag_service.generate_grounded_answer(question=question, top_k=5)

            # 2. Extract retrieved document IDs
            retrieved_doc_ids = list(dict.fromkeys([
                c.get("document_id") for c in rag_res.get("citations", []) if c.get("document_id")
            ] + [
                chunk.get("document_id") for chunk in self.hybrid_pipeline.search(question, top_k=5).get("top_chunks", []) if chunk.get("document_id")
            ]))

            # 3. Compute Metrics
            p1 = calculate_precision_at_k(retrieved_doc_ids, expected_doc_ids, k=1)
            p3 = calculate_precision_at_k(retrieved_doc_ids, expected_doc_ids, k=3)
            p5 = calculate_precision_at_k(retrieved_doc_ids, expected_doc_ids, k=5)

            r1 = calculate_recall_at_k(retrieved_doc_ids, expected_doc_ids, k=1)
            r3 = calculate_recall_at_k(retrieved_doc_ids, expected_doc_ids, k=3)
            r5 = calculate_recall_at_k(retrieved_doc_ids, expected_doc_ids, k=5)

            rr = calculate_reciprocal_rank(retrieved_doc_ids, expected_doc_ids)
            g_score = rag_res.get("grounding_score", 0.0)

            p1_list.append(p1)
            p3_list.append(p3)
            p5_list.append(p5)
            r1_list.append(r1)
            r3_list.append(r3)
            r5_list.append(r5)
            mrr_list.append(rr)
            groundedness_list.append(g_score)

            results.append({
                "test_case_id": tc_id,
                "category": tc["category"],
                "question": question,
                "expected_doc_ids": expected_doc_ids,
                "retrieved_doc_ids": retrieved_doc_ids[:5],
                "precision_at_3": p3,
                "recall_at_3": r3,
                "reciprocal_rank": rr,
                "grounding_score": g_score,
                "is_grounded": rag_res.get("is_grounded", False),
                "citations_count": rag_res.get("citations_count", 0),
            })

        avg_p1 = round(sum(p1_list) / len(p1_list), 4) if p1_list else 0.0
        avg_p3 = round(sum(p3_list) / len(p3_list), 4) if p3_list else 0.0
        avg_p5 = round(sum(p5_list) / len(p5_list), 4) if p5_list else 0.0

        avg_r1 = round(sum(r1_list) / len(r1_list), 4) if r1_list else 0.0
        avg_r3 = round(sum(r3_list) / len(r3_list), 4) if r3_list else 0.0
        avg_r5 = round(sum(r5_list) / len(r5_list), 4) if r5_list else 0.0

        mrr = round(sum(mrr_list) / len(mrr_list), 4) if mrr_list else 0.0
        avg_groundedness = round(sum(groundedness_list) / len(groundedness_list), 4) if groundedness_list else 0.0

        summary = {
            "total_benchmark_cases": len(results),
            "precision_at_1": avg_p1,
            "precision_at_3": avg_p3,
            "precision_at_5": avg_p5,
            "recall_at_1": avg_r1,
            "recall_at_3": avg_r3,
            "recall_at_5": avg_r5,
            "mean_reciprocal_rank": mrr,
            "mean_groundedness_score": avg_groundedness,
            "groundedness_pass_rate": round(sum(1 for g in groundedness_list if g >= 0.70) / len(groundedness_list), 4) if groundedness_list else 0.0,
            "test_cases": results
        }

        return summary


def get_evaluator() -> BenchmarkEvaluator:
    global _evaluator_instance
    if _evaluator_instance is None:
        _evaluator_instance = BenchmarkEvaluator()
    return _evaluator_instance
