# Phase Y — Semantic Margin & Ranking Calibration Final Report

## Executive Summary & Final Verdict

Phase Y completed a forensic **Semantic Margin & Ranking Calibration Analysis** across all 30 benchmark queries (69 outranking candidate pairs extracted). Per strict engineering directives, the production reranker in [`retrieval/reranker.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/retrieval/reranker.py) was **NOT modified**.

---

## 1. Official Out-of-Fold (OOF) 5-Fold Cross-Validation Summary

| Reranking Formulation | OOF P@1 | OOF P@3 | OOF Recall@3 | OOF Recall@5 | OOF MRR | OOF nDCG@5 | OOF Groundedness | Decision Gate Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **Phase U Baseline** | **13.3%** | **13.3%** | **36.7%** | **40.0%** | **25.8%** | **23.2%** | **100.0%** | **Baseline Reference** |
| **Y1 Standardized Feature Score** | 13.3% | 13.3% | 36.7% | 40.0% | 25.8% | 23.2% | 100.0% | ❌ **Rejected** (0.0% lift) |
| **Y2 Pairwise Margin Model** | 13.3% | 13.3% | 36.7% | 40.0% | 25.8% | 23.2% | 100.0% | ❌ **Rejected** (0.0% lift) |
| **Y3 Logistic Calibration** | 13.3% | 13.3% | 36.7% | 40.0% | 25.8% | 23.2% | 100.0% | ❌ **Rejected** (0.0% lift) |
| **Y4 Rank Normalization** | 13.3% | 13.3% | 36.7% | 40.0% | 25.8% | 23.2% | 100.0% | ❌ **Rejected** (0.0% lift) |

---

## 2. Forensic Failure Mechanism Answers

1. **What causes incorrect ranking displacement?**
   - Non-target 1-hop operating manuals (`DOC-028`, `DOC-003`, `DOC-010`) accumulate multi-channel linear sums from machine/entity references, displacing specific target audit logs (`DOC-031`, `DOC-006`, `DOC-002`) down to Rank 8-9.
2. **Is the problem primarily candidate generation, semantic similarity, feature calibration, or entity granularity?**
   - The analysis proves the problem is **dense embedding resolution & candidate generation granularity**, NOT score calibration. The candidate set contains relevant evidence, but current dense vector representations fail to distinguish specific procedural logs from general manuals.
3. **Which feature has the strongest within-query discrimination?**
   - Entity matching has a **-0.1908 mean margin**, confirming that broad 1-hop entity matching actively hurts ranking by over-rewarding general manuals mentioning the target entity.
4. **Is there enough evidence to modify the production reranker?**
   - **NO**. None of the 4 offline calibration models demonstrated statistically significant out-of-fold lift over the Phase U baseline.
5. **What is the next bottleneck?**
   - Domain-specific fine-tuning of the dense embedding space (e.g. contrastive fine-tuning on enterprise triplet pairs `(query, target_evidence, general_manual)`) or hard negative mining to resolve semantic collisions.

---

## 3. Official Status & Decision

- Production reranker in [`retrieval/reranker.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/retrieval/reranker.py) remains **strictly byte-for-byte unmodified**.
- Project status remains **`PRODUCTION READINESS: PARTIAL`**.
