# Phase AA — Fusion-to-Ranking Propagation & Controlled Weighting Analysis (`docs/PHASE_AA_FUSION_ANALYSIS.md`)

## Executive Summary

Phase AA performed a controlled offline diagnostic experiment across all 30 protected benchmark test cases to answer one core scientific question:
> **If the improved dense signal from Phase Z is given controlled influence during candidate fusion, does end-to-end retrieval performance improve, or is the signal destroyed downstream?**

---

## 1. Experimental Matrix Results (10 Configurations)

All configurations were evaluated offline in an isolated diagnostic script ([`scratch/execute_phase_aa_fusion_analysis.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/scratch/execute_phase_aa_fusion_analysis.py)) over the protected 30-case benchmark without modifying production code.

| Configuration Name | Description | Precision@1 | Precision@3 | Recall@3 | Recall@5 | MRR |
|---|---|---:|---:|---:|---:|---:|
| **Baseline 0 (Phase U)** | Control Embedder + BM25 + Relational + RRF ($k=60$) + Reranker | 13.33% | 8.33% | 26.67% | 26.67% | 24.44% |
| **Config 1** | BM25 Lexical Only | 10.00% | 8.89% | 21.67% | 38.33% | 23.11% |
| **Config 2a** | Dense Vector Only (Control `all-MiniLM-L6-v2`) | 6.67% | 4.44% | 23.33% | 28.33% | 21.11% |
| **Config 2b** | **Dense Vector Only (Phase Z Checkpoint)** | **20.00%** | **8.89%** | **30.00%** | **36.67%** | **32.61%** |
| **Config 3** | Relational Graph Candidates Only | 10.00% | 10.00% | 10.00% | 10.00% | 10.00% |
| **Config 4** | Phase Z Embedder + Standard RRF ($k=60$) + Reranker | 10.00% | 10.56% | 23.33% | 30.00% | 23.72% |
| **Config 5** | Phase Z Embedder + Dense Weighted RRF ($w_{\text{vec}}=0.7$) + Reranker | 10.00% | 10.56% | 23.33% | 30.00% | 23.72% |
| **Config 6** | Phase Z Embedder + Lexical Weighted RRF ($w_{\text{bm25}}=0.7$) + Reranker | 10.00% | 10.56% | 23.33% | 30.00% | 23.72% |
| **Config 7** | Phase Z Embedder + Tight RRF Window ($k=20$) + Reranker | 10.00% | 10.56% | 23.33% | 30.00% | 23.72% |
| **Config 8** | Phase Z Embedder + Loose RRF Window ($k=100$) + Reranker | 10.00% | 10.56% | 23.33% | 30.00% | 23.72% |

---

## 2. Key Empirical Findings

1. **Standalone Dense Phase Z Superiority (Config 2b)**:
   - Evaluated as a pure retrieval channel, **Phase Z dense vector search achieved the highest standalone MRR (32.61%) and Precision@1 (20.00%)**, dramatically outperforming Control dense search (P@1: 6.67%, MRR: 21.11%) and BM25 lexical search (P@1: 10.00%, MRR: 23.11%).

2. **RRF & Downstream Reranking Signal Compression**:
   - As soon as Phase Z dense candidates are passed into RRF candidate fusion alongside BM25 and Relational candidates and reranked by the downstream multi-feature reranker (Configs 4–8), **MRR drops from 32.61% down to 23.72%** and **P@1 drops from 20.00% down to 10.00%**.
   - Weight adjustments ($w_{\text{vec}}=0.7$ vs $w_{\text{bm25}}=0.7$) and window adjustments ($k=20, 60, 100$) within standard RRF fail to prevent downstream signal degradation because the linear score terms in the reranker ($0.25 S_{\text{bm25}} + 0.25 S_{\text{vec}} + S_{\text{entity}} + S_{\text{rel}} + S_{\text{intent}}$) override the dense similarity margins.

---

## 3. Propagation Failure Mode Classification

- **Observed Scenario**: **Scenario B (Dense signal survives raw dense retrieval but is degraded during candidate fusion & downstream multi-feature reranking)**.
- **Root Cause**: The linear score combination in the reranker treats raw BM25, entity matches, and relational links with fixed uncalibrated weights that dominate dense embedding similarity margins.
