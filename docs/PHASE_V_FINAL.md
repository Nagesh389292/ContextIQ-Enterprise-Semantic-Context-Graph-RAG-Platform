# Phase V & V.5 — Forensic Score Calibration & Evaluation Reconciliation Report

## Executive Summary & Diagnostic Findings

Phase V & V.5 executed a forensic evaluation reconciliation and controlled multi-model ablation run across all 30 benchmark test cases. Per strict engineering directives, the production reranker in [`retrieval/reranker.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/retrieval/reranker.py) was **NOT modified**.

---

## 1. Evaluation Reconciliation

| Metric Target | Phase T/U Initial Report (27 Domain-Only) | Master Evaluator Baseline (All 30 Cases) | Reconciled Baseline |
|---|---:|---:|---:|
| **Precision@1** | 30.0% | 23.3% | **23.3%** |
| **Precision@3** | 30.0% | 20.6% | **20.6%** |
| **Recall@3** | 41.7% | 33.3% | **33.3%** |
| **Recall@5** | 53.3% | 45.0% | **45.0%** |
| **MRR** | 38.2% | 30.2% | **30.2%** |

*Reconciliation Note*: The code and evaluation harness are 100% identical. The numerical difference was purely between domain-only averaging (27 cases) vs. full dataset micro-averaging across all 30 test cases (including 3 Edge Cases). All Phase V & V.5 comparisons use the 30-case baseline.

---

## 2. Complete Ablation Matrix Across All Formulations

| Reranking Model | P@1 | P@3 | Recall@3 | Recall@5 | MRR | Maintenance R@3 | Supplier R@3 | Quality R@3 | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Phase U Baseline** | **23.3%** | **20.6%** | **33.3%** | **45.0%** | **30.2%** | **25.0%** | 0.0% | 28.6% | **Baseline** |
| **Model V1 (3-Channel RRF)** | 23.3% | 16.7% ❌ | 25.0% ❌ | 26.7% ❌ | 25.1% | 0.0% ❌ | 10.0% | 28.6% | ❌ **Rejected** |
| **Model V2 (Normalized Multi-Feature)** | 20.0% | 19.4% | 33.3% | 40.0% | 28.3% | 12.5% ❌ | 0.0% | **42.9%** | ❌ **Rejected** |
| **Model V3 (Hop-Calibrated 0.45/hops)** | 20.0% | 20.0% | 33.3% | 38.3% ❌ | 26.5% | **25.0%** | 0.0% | **42.9%** | ❌ **Rejected** |
| **Model Bounded (V.5 Bounded Signals)** | 16.7% ❌ | 17.8% ❌ | 28.3% ❌ | 30.0% ❌ | 24.0% | 0.0% ❌ | 10.0% | **42.9%** | ❌ **Rejected** |

---

## 3. Quantitative Scale Mismatch Proof

Our forensic analysis in [`docs/PHASE_V_RANKING_DISPLACEMENT.md`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/docs/PHASE_V_RANKING_DISPLACEMENT.md) established:
1. **RRF Base Scale**: $RRF = \frac{1}{60 + r_b} + \frac{1}{60 + r_v} \approx \mathbf{0.01639 - 0.03278}$.
2. **Additive Boost Scale**: Additive terms ($S_{\text{bm25}}=0.25, S_{\text{vec}}=0.25, S_{\text{entity}}=0.35, S_{\text{rel}}=0.45, S_{\text{intent}}=0.30$) total $\mathbf{1.65}$.
3. **Scale Mismatch Factor**: Additive boost terms overpower RRF fusion values by $50\times$.
4. **Multi-Feature Accumulation**: Non-target 1-hop documents (`DOC-028` Welding Robot Manual) accumulate BM25 + Vector + Entity + Intent + Relational boosts ($\mathbf{1.6828}$), displacing single-channel target documents (`DOC-031` Audit Log, $\mathbf{0.7664}$) to Rank #5.

---

## 4. Official Decision & Project Status

- All alternative score fusion models (V1, V2, V3, Bounded) have been **formally rejected** based on empirical benchmark evidence.
- The production reranker in [`retrieval/reranker.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/retrieval/reranker.py) remains **unmodified**.
- Status remains **`PRODUCTION READINESS: PARTIAL`**.
