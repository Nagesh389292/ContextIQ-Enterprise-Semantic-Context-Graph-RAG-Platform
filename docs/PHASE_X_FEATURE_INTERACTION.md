# Phase X — Query-Grouped Feature Interaction Cross-Validation Report (`docs/PHASE_X_FEATURE_INTERACTION.md`)

## Executive Summary & Methodology

Phase X evaluated candidate feature interactions via **Query-Grouped 5-Fold Cross-Validation** across all 30 benchmark test cases (5 folds of 6 queries each). This prevents candidate chunk-level data leakage across training/validation sets.

---

## 1. Out-of-Fold (OOF) Metric Comparison Matrix

| Reranking Formulation | OOF P@1 | OOF P@3 | OOF Recall@3 | OOF Recall@5 | OOF MRR | OOF nDCG@5 | Supplier R@3 | Quality R@3 | Out-of-Fold Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Phase U Baseline** | **23.3%** | 20.6% | 33.3% | **45.0%** | **30.2%** | **33.7%** | 0.0% | 28.6% | **Baseline Reference** |
| **Model X1 (Pairwise $I_1 = \text{rel} \times \text{intent}$)** | **23.3%** | **21.7%** ↗ | **35.0%** ↗ | 40.0% ❌ | **30.2%** | 32.3% ❌ | **10.0%** ↗ | **42.9%** ↗ | 🔬 **Directional Only** |
| **Model X4 (Combined $I_1+I_4+I_7$)** | **23.3%** | 19.4% ❌ | 30.0% ❌ | 38.3% ❌ | 28.8% ❌ | 31.1% ❌ | 0.0% | 28.6% | ❌ **Rejected** |

---

## 2. Fold-by-Fold Out-of-Fold Breakdown

### Fold 2 Breakdown (Test Cases TC-007 to TC-012)
- **Baseline**: Val P@3: 13.9%, Val R@3: 33.3%, Val R@5: 50.0%, Val MRR: 0.1805
- **Model X1**: Val P@3: **19.4%**, Val R@3: **50.0%**, Val R@5: 50.0%, Val MRR: **0.3055**
- *Insight*: Pairwise interaction $I_1$ successfully promoted target maintenance evidence (`DOC-031`) into top-3 in held-out validation queries without leakage.

### Fold 4 Breakdown (Test Cases TC-019 to TC-024)
- **Baseline**: Val P@3: 8.3%, Val R@3: 16.7%, Val R@5: 33.3%, Val MRR: 0.2000
- **Model X1**: Val P@3: **13.9%**, Val R@3: **25.0%**, Val R@5: **41.7%**, Val MRR: **0.2555**
- *Insight*: Supplier contract relationships (`DOC-006`) were promoted into top-3 in held-out queries.

---

## 3. Why Model X1 is NOT Sufficient for Production

Although `Model X1` achieved held-out gains on Recall@3 (+1.7%) and Supplier Recall@3 (+10.0%), out-of-fold evaluation exposed two critical weaknesses:
1. **Recall@5 Drop**: Out-of-fold Recall@5 dropped from **45.0% $\rightarrow$ 40.0%** (-5.0 percentage points).
2. **nDCG@5 Drop**: Out-of-fold nDCG@5 dropped from **33.7% $\rightarrow$ 32.3%** (-1.4 percentage points).

---

## 4. Official Decision & Status

- `Model X1` is confirmed as a **directional winner, but not a production winner**.
- Production reranker in [`retrieval/reranker.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/retrieval/reranker.py) remains **unmodified**.
- Status remains **`PRODUCTION READINESS: PARTIAL`**.
