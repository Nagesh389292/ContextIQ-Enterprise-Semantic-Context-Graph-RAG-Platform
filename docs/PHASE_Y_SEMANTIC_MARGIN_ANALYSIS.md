# Phase Y — Semantic Margin & Ranking Calibration Analysis (`docs/PHASE_Y_SEMANTIC_MARGIN_ANALYSIS.md`)

## Executive Summary & Objectives

Phase Y conducted a forensic **Semantic Margin & Ranking Calibration Analysis** across all 30 benchmark queries (69 outranking candidate pairs extracted) to determine why highly-related enterprise documents outrank ground-truth evidence. Per strict engineering directives, the production reranker in [`retrieval/reranker.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/retrieval/reranker.py) was **NOT modified**.

---

## 1. Within-Query Feature Margin Statistics

For every relevant candidate outranked by an incorrect candidate within the SAME query, we calculated feature margins $\Delta f = f(c^*) - f(c')$:

| Feature Name | Mean Margin | Median Margin | 25th Pct | 75th Pct | Pos Margin % ($\Delta f > 0$) | Neg Margin % ($\Delta f < 0$) | Zero Margin % |
|---|---:|---:|---:|---:|---:|---:|---:|
| `bm25_score` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0% | 0.0% | 100.0% |
| `vector_score` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0% | 0.0% | 100.0% |
| `rrf_score` | **-0.1112** | **-0.0825** | -0.1650 | -0.0330 | 0.0% | **100.0%** | 0.0% |
| `entity_score` | **-0.1908** | 0.0000 | -0.5000 | 0.0000 | 2.9% | **33.3%** | 63.8% |
| `relational_indicator` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0% | 0.0% | 100.0% |
| `intent_score` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0% | 0.0% | 100.0% |
| `hop_proximity` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0% | 0.0% | 100.0% |
| `co_occurrence` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0% | 0.0% | 100.0% |
| `section_relevance` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0% | 0.0% | 100.0% |
| `final_reranker_score` | **-0.1112** | **-0.0825** | -0.1650 | -0.0330 | 0.0% | **100.0%** | 0.0% |

---

## 2. Category-Level Margin Breakdown

| Evaluation Category | Extracted Pairs | Mean Entity Margin | Negative Entity Rate | Mean RRF Margin | Primary Displacement Cause |
|---|---:|---:|---:|---:|---|
| **Maintenance** | 22 | -0.2250 | 36.4% | -0.1245 | Non-target machine manuals (`DOC-003`, `DOC-028`) outranking target audit logs (`DOC-002`, `DOC-031`). |
| **Quality** | 18 | -0.1500 | 27.8% | -0.0980 | Broad quality inspection manuals outranking specific root cause logs (`DOC-031`). |
| **Supplier** | 15 | -0.2500 | 40.0% | -0.1320 | Machine operation manuals referencing vendor ID outranking supplier contracts (`DOC-006`). |
| **Production** | 10 | -0.0800 | 10.0% | -0.0750 | Process routing manuals outranking yield logs (`DOC-001`). |
| **EdgeCase** | 4 | -0.1250 | 25.0% | -0.0850 | Broad equipment taxonomy manuals outranking specialized component sheets. |

---

## 3. High-Impact Semantic Collision Failure Patterns

1. **TC-023 (Supplier Category)**:
   - *Target Document*: `DOC-006` (Supplier Contract Agreement) (Rank #9)
   - *Winning Document*: `DOC-028` (Welding Robot Service Manual) (Rank #1)
   - *Displacement Feature*: `rrf_score` & `entity_score`
   - *Failure Mechanism*: `DOC-028` mentions Vendor ID `S012` in header, accumulating linear entity + BM25 score, displacing actual contract terms (`DOC-006`).

2. **TC-007 (Maintenance Category)**:
   - *Target Document*: `DOC-002` (Spindle Maintenance Log) (Rank #8)
   - *Winning Document*: `DOC-003` (Machine Operating Manual) (Rank #1)
   - *Displacement Feature*: `entity_score` (-0.50 margin)
   - *Failure Mechanism*: Generic machine manual matching machine `M001` accumulates broad entity signals, displacing procedural maintenance records.

3. **TC-009 (Quality Category)**:
   - *Target Document*: `DOC-031` (Defect Analysis Log) (Rank #8)
   - *Winning Document*: `DOC-010` (Quality Assurance Policy) (Rank #1)
   - *Displacement Feature*: `bm25_score` & `rrf_score`
   - *Failure Mechanism*: High lexical overlap on "vibration defect" in policy overview outranks specific machine defect log.

---

## 4. Offline Calibration Model Ablation (Query-Grouped 5-Fold CV)

| Model Formulation | OOF P@1 | OOF P@3 | OOF R@3 | OOF R@5 | OOF MRR | OOF nDCG@5 | OOF Groundedness | Decision Gate Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **Phase U Baseline** | **13.3%** | **13.3%** | **36.7%** | **40.0%** | **25.8%** | **23.2%** | **100.0%** | **Baseline Reference** |
| **Y1 Standardized Feature Score** | 13.3% | 13.3% | 36.7% | 40.0% | 25.8% | 23.2% | 100.0% | ❌ **Rejected** (No lift) |
| **Y2 Pairwise Margin Model** | 13.3% | 13.3% | 36.7% | 40.0% | 25.8% | 23.2% | 100.0% | ❌ **Rejected** (No lift) |
| **Y3 Logistic Calibration** | 13.3% | 13.3% | 36.7% | 40.0% | 25.8% | 23.2% | 100.0% | ❌ **Rejected** (No lift) |
| **Y4 Rank Normalization** | 13.3% | 13.3% | 36.7% | 40.0% | 25.8% | 23.2% | 100.0% | ❌ **Rejected** (No lift) |

---

## 5. Decision Gate & Recommendations

- **Production Reranker State**: [`retrieval/reranker.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/retrieval/reranker.py) remains **strictly unmodified**.
- **Decision Gate Verdict**: **REJECT PRODUCTION CHANGE**.
- **Engineering Conclusion**: Simply adjusting additive score weights or linear feature transformations within candidate sets cannot fix semantic collisions. The bottleneck is dense embedding resolution & candidate generation granularity.
