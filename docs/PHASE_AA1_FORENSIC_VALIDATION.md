# Phase AA.1 — Evaluation Reconciliation & Fusion Parameter Propagation Forensics (`docs/PHASE_AA1_FORENSIC_VALIDATION.md`)

## Executive Summary

Phase AA.1 conducted a forensic diagnostic audit of the evaluation harness to resolve the baseline discrepancy and parameter propagation issues identified in Phase AA.

---

## 1. Baseline Reconciliation Audit (Step 1)

| Benchmark Source | Precision@1 | Precision@3 | Recall@3 | Recall@5 | MRR | Groundedness | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| **Official `BenchmarkEvaluator` (Phase U / Phase Y.1 / Phase AA.1)** | **23.33%** | **20.56%** | **33.33%** | **45.00%** | **30.22%** | **100.0%** | **RECONCILED (100% Exact Match)** |
| **Phase AA Custom Harness Baseline (Old)** | 13.33% | 8.33% | 26.67% | 26.67% | 24.44% | N/A | Discrepancy Identified & Fixed |

### Cause of Baseline Discrepancy:
1. **Edge Case Query Scoring (TC-028, TC-029, TC-030)**: In the official `BenchmarkEvaluator`, edge cases produce 0 citations (`retrieved_doc_ids = []`). When `expected_doc_ids = []` and `retrieved_doc_ids = []`, `precision_at_k` and `recall_at_k` return `1.0` (correct zero-retrieval for negative queries). The old Phase AA custom loop did not strip un-cited candidates for negative queries, scoring them as `0.0`.
2. **Document-Level vs Chunk-Level ID Matching**: `BenchmarkEvaluator` evaluates document-level IDs (`DOC-MNT-001`), whereas the old diagnostic script evaluated raw chunk IDs (`DOC-MNT-001_c1`).

---

## 2. Parametric Candidate Pool Fusion Audit (Step 2)

### Root Cause of Identical Config 4–8 Metrics in Phase AA:
In the original Phase AA script, the custom RRF fusion function produced a fused candidate list (`fused`), but `production_reranker.rerank()` was called directly with raw `bm25_res` and `vec_res`, completely bypassing `fused`! Consequently, RRF weights ($w_{\text{vec}}$, $w_{\text{bm25}}$) and window size ($k$) were never passed to the reranking stage.

### Corrected Parametric Fusion Results (Phase AA.1):

| Configuration | Description | P@1 | P@3 | R@3 | R@5 | MRR |
|---|---|---:|---:|---:|---:|---:|
| **Official Baseline** | Official Production Hybrid Pipeline | **23.33%** | **20.56%** | **33.33%** | **45.00%** | **30.22%** |
| **V1** | BM25 Lexical Only | 10.00% | 8.89% | 21.67% | 28.33% | 20.78% |
| **V2a** | Control Dense Vector Only (`all-MiniLM-L6-v2`) | 6.67% | 5.00% | 23.33% | 28.33% | 21.11% |
| **V2b** | **Phase Z Dense Vector Only (`artifacts/phase_z/checkpoint`)** | **20.00%** | **11.11%** | **26.67%** | **26.67%** | **30.00%** |
| **V3** | Phase Z + Standard RRF ($k=60$) | 10.00% | 7.78% | 26.67% | 36.67% | 26.06% |
| **V4** | Phase Z + Dense-Weighted RRF ($w_{\text{vec}}=0.7, w_{\text{bm25}}=0.3$) | 13.33% | 5.56% | 20.00% | 30.00% | 25.67% |
| **V5** | Phase Z + Lexical-Weighted RRF ($w_{\text{bm25}}=0.7, w_{\text{vec}}=0.3$) | 10.00% | 6.67% | 25.00% | 36.67% | 25.39% |
| **V6** | Phase Z + Tight RRF Window ($k=20$) | 10.00% | 7.78% | 26.67% | 33.33% | 25.39% |
| **V7** | Phase Z + Loose RRF Window ($k=100$) | 10.00% | 7.78% | 26.67% | 36.67% | 26.06% |

---

## 3. Key Findings

1. **Parametric Changes NOW Actively Alter Rankings**:
   - Dense weighting ($w_{\text{vec}}=0.7$, V4) increased Precision@1 from 10.00% to **13.33%**.
   - Tight RRF window ($k=20$, V6) vs Loose RRF window ($k=100$, V7) shifts Recall@5 between 33.33% and 36.67%.
2. **Phase Z Dense Search Superiority Confirmed**:
   - In pure standalone vector search, Phase Z embeddings achieved **30.00% MRR** and **20.00% P@1** vs Control dense search (**21.11% MRR**, **6.67% P@1**).
