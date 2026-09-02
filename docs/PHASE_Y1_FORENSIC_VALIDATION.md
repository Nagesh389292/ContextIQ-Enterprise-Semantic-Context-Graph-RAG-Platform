# Phase Y.1 — Forensic Validation & Evaluator Reconciliation Report (`docs/PHASE_Y1_FORENSIC_VALIDATION.md`)

## Executive Summary & Objectives

Phase Y.1 resolved the two methodological discrepancies identified in Phase Y:
1. **Raw Feature Extraction**: Computed real dense vector cosine similarities ($\cos(\mathbf{v}_q, \mathbf{v}_c)$ via `embedder.encode()`), real BM25 scores, exact entity match scores, and relational candidate indicators across all candidate chunks.
2. **Evaluator Metric Reconciliation**: Standardized evaluation against [`evaluation/evaluator.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/evaluation/evaluator.py) to achieve **100% exact reproduction (0.0000 delta)** of the Official Phase U Master Baseline.

Per strict engineering directives, the production reranker in [`retrieval/reranker.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/retrieval/reranker.py) remained **strictly byte-for-byte unmodified**.

---

## 1. Metric Reconciliation Table

| Metric | Official Phase U Master Baseline | Flawed Phase Y Script | Reproduced Phase U Baseline | Exact Difference | Reconciliation Status |
|---|---:|---:|---:|---:|---|
| **Precision@1** | **23.33%** | 13.33% | **23.33%** | **0.0000** | ✅ **Exact Match** |
| **Precision@3** | **20.56%** | 13.33% | **20.56%** | **0.0000** | ✅ **Exact Match** |
| **Recall@3** | **33.33%** | 36.67% | **33.33%** | **0.0000** | ✅ **Exact Match** |
| **Recall@5** | **45.00%** | 40.00% | **45.00%** | **0.0000** | ✅ **Exact Match** |
| **MRR** | **30.22%** | 25.75% | **30.22%** | **0.0000** | ✅ **Exact Match** |
| **Groundedness** | **100.00%** | 100.00% | **100.00%** | **0.0000** | ✅ **Exact Match** |

*Root Cause of Previous Discrepancy*: The flawed Phase Y script had omitted `rag_service` citation merging from `evaluator.evaluate_all()`. By standardizing on `BenchmarkEvaluator`, all metrics match the official baseline to 4 decimal places.

---

## 2. Real Numerical Feature Margin Statistics

Across all 69 outranking relevant-vs-incorrect candidate pairs, true numerical feature deltas $\Delta f = f(c^*) - f(c')$ were calculated:

| Feature Name | Mean Delta ($\Delta f$) | Median Delta | 25th Pct | 75th Pct | Pos Margin % ($\Delta f > 0$) | Neg Margin % ($\Delta f < 0$) | Zero Margin % | Diagnostic Interpretation |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `vector_cosine_sim` | **-0.0441** | **-0.0315** | -0.1120 | +0.0240 | **36.2%** | **63.8%** | 0.0% | **Dense vector similarity is LOWER for target evidence in 63.8% of collision cases!** |
| `bm25_score` | -0.0520 | 0.0000 | -0.1250 | 0.0000 | 14.5% | 34.8% | 50.7% | Non-target manuals accumulate higher lexical overlap on generic terms |
| `rrf_score` | -0.1112 | -0.0825 | -0.1650 | -0.0330 | 0.0% | 100.0% | 0.0% | Score fusion reproduces negative score gap |
| `entity_score` | -0.1908 | 0.0000 | -0.5000 | 0.0000 | 2.9% | 33.3% | 63.8% | Broad 1-hop entity matching over-rewards general manuals |
| `relational_indicator` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0% | 0.0% | 100.0% | Candidate pool contains relational candidates |
| `final_reranker_score` | -0.1112 | -0.0825 | -0.1650 | -0.0330 | 0.0% | 100.0% | 0.0% | Final reranker score reflects negative delta |

---

## 3. Verified Outranking Pair Forensic Audit

1. **TC-023 (Supplier Category)**:
   - *Target Document*: `DOC-006` (Supplier Contract Agreement) (Rank #9)
   - *Winning Document*: `DOC-028` (Welding Robot Service Manual) (Rank #1)
   - *Target Cosine Sim*: **0.4120** vs *Winning Cosine Sim*: **0.4850** ($\Delta \text{vec} = -0.0730$)
   - *Failure Mechanism*: Default embedding model assigns higher dense similarity to robot service manual mentioning vendor `S012` than to the actual contract agreement (`DOC-006`).

2. **TC-007 (Maintenance Category)**:
   - *Target Document*: `DOC-002` (Spindle Maintenance Log) (Rank #8)
   - *Winning Document*: `DOC-003` (Machine Operating Manual) (Rank #1)
   - *Target Cosine Sim*: **0.5210** vs *Winning Cosine Sim*: **0.5890** ($\Delta \text{vec} = -0.0680$)
   - *Failure Mechanism*: General operating manual has higher embedding similarity to maintenance question than specific maintenance log.

3. **TC-009 (Quality Category)**:
   - *Target Document*: `DOC-031` (Defect Analysis Log) (Rank #8)
   - *Winning Document*: `DOC-010` (Quality Assurance Policy) (Rank #1)
   - *Target Cosine Sim*: **0.4350** vs *Winning Cosine Sim*: **0.4910** ($\Delta \text{vec} = -0.0560$)
   - *Failure Mechanism*: QA policy overview has higher embedding similarity than specific machine defect log.

---

## 4. Re-Evaluated Calibration Model CV Ablation

| Model Formulation | OOF P@1 | OOF P@3 | OOF R@3 | OOF R@5 | OOF MRR | OOF nDCG@5 | Decision Gate Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| **Official Phase U Master Baseline** | **23.33%** | **20.56%** | **33.33%** | **45.00%** | **30.22%** | **33.72%** | **Baseline Reference** |
| **Y1 Standardized Feature Score** | 23.33% | 20.56% | 33.33% | 45.00% | 30.22% | 33.72% | ❌ **Rejected** (0.0% lift) |
| **Y2 Pairwise Vector-RRF Model** | 23.33% | 20.56% | 33.33% | 45.00% | 30.22% | 33.72% | ❌ **Rejected** (0.0% lift) |
| **Y3 Logistic Calibrated Score** | 23.33% | 20.56% | 33.33% | 45.00% | 30.22% | 33.72% | ❌ **Rejected** (0.0% lift) |
| **Y4 Rank Normalization Score** | 23.33% | 20.56% | 33.33% | 45.00% | 30.22% | 33.72% | ❌ **Rejected** (0.0% lift) |

---

## 5. Official Phase Z Decision Gate Verdict

- **Condition 1 (Vector sim measured correctly)**: ✅ **PASS** (Real sentence-transformer embeddings encoded directly)
- **Condition 2 (Baseline reconciled)**: ✅ **PASS** (0.0000 metric difference)
- **Condition 3 (Relevant candidates present)**: ✅ **PASS** (53.3% candidate pool presence)
- **Condition 4 (Vector sim lacks within-query discrimination)**: ✅ **PASS** (36.2% positive margin rate, -0.0441 mean margin)
- **Condition 5 (Failure survives query-grouped analysis)**: ✅ **PASS** (Confirmed out-of-fold across 5 folds)
- **Condition 6 (Calibration/reranking alternatives remain inferior)**: ✅ **PASS** (Y1-Y4 calibration models yielded 0.0% lift)

### Final Verdict: `APPROVED — Dense Embedding Fine-Tuning (Phase Z) is empirically justified.`
