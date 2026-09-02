"""
ContextIQ — Evaluation Metrics Calculator
Computes Precision@k, Recall@k, Mean Reciprocal Rank (MRR), and Groundedness Scores.
"""

from typing import List, Dict, Any


def calculate_precision_at_k(retrieved_doc_ids: List[str], expected_doc_ids: List[str], k: int) -> float:
    """Calculate Precision at top k retrieved documents."""
    if not expected_doc_ids or k <= 0:
        return 1.0 if not retrieved_doc_ids else 0.0

    retrieved_at_k = retrieved_doc_ids[:k]
    if not retrieved_at_k:
        return 0.0

    # Count unique relevant documents retrieved at rank k
    unique_retrieved_at_k = list(dict.fromkeys(retrieved_at_k))
    relevant_retrieved = sum(1 for doc_id in unique_retrieved_at_k if doc_id in expected_doc_ids)
    return round(relevant_retrieved / len(unique_retrieved_at_k), 4)


def calculate_recall_at_k(retrieved_doc_ids: List[str], expected_doc_ids: List[str], k: int) -> float:
    """Calculate Recall at top k retrieved documents."""
    if not expected_doc_ids:
        return 1.0

    retrieved_at_k = retrieved_doc_ids[:k]
    if not retrieved_at_k:
        return 0.0

    # Count unique relevant documents retrieved at rank k
    unique_retrieved_at_k = list(dict.fromkeys(retrieved_at_k))
    relevant_retrieved = sum(1 for doc_id in unique_retrieved_at_k if doc_id in expected_doc_ids)
    recall = relevant_retrieved / len(expected_doc_ids)
    return round(min(1.0, recall), 4)


def calculate_reciprocal_rank(retrieved_doc_ids: List[str], expected_doc_ids: List[str]) -> float:
    """Calculate Reciprocal Rank (1/rank of first relevant document)."""
    if not expected_doc_ids:
        return 1.0

    for rank, doc_id in enumerate(retrieved_doc_ids, start=1):
        if doc_id in expected_doc_ids:
            return round(1.0 / rank, 4)

    return 0.0
