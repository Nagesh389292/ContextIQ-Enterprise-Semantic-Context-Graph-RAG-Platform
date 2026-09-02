# ContextIQ — Phase T Final Forensic Engineering Report (`docs/PHASE_T_FINAL.md`)

## 1. Executive Summary
Phase T — Retrieval Dataset & Ground-Truth Engineering has completed a forensic, unmocked diagnostic audit across all 30 benchmark test cases. No retrieval scoring weights, reranking algorithms, embedding models, or ground-truth definitions were altered during this diagnostic phase. The audit conclusively identified why Maintenance (12.5% Recall@3) and Supplier (30.0% Recall@3) retrieval fail.

## 2. Verified Unmocked Metrics (Unique Document Recall)

| Metric | Production | Quality | Supplier | Maintenance | **Overall Baseline** |
|---|---:|---:|---:|---:|---:|
| **Precision@1** | 42.9% | 14.3% | 20.0% | 12.5% | **30.0%** |
| **Precision@3** | 38.1% | 23.8% | 20.0% | 8.3% | **30.0%** |
| **Recall@3** | 57.1% | 42.9% | **30.0%** ❌ | **12.5%** ❌ | **41.7%** ❌ |
| **Recall@5** | 57.1% | 71.4% | **30.0%** ❌ | **31.2%** ❌ | **53.3%** ❌ |
| **MRR** | 50.0% | 31.0% | 26.7% | 18.1% | **38.2%** |
| **Groundedness** | 99.2% | 99.2% | 99.2% | 99.2% | **99.2%** |

## 3. Key Forensic Discoveries & Failure Audits
1. **Candidate Generation & Graph Traversal Gap**: For Maintenance test cases (e.g. TC-001 expecting `DOC-031`), `DOC-028` (*Welding Robot Manual M001*) lexically and semantically dominates BM25 and vector search due to high frequency of machine identifier `M001`. `DOC-031` (*Plant P003 Batch Audit*) documents defect logs for M001, but lacks direct text matches for 'maintenance procedure'. Graph expansion Cypher traversals currently lack explicit multi-hop joins connecting `M001 -[:PRODUCES_ORDER]-> PO-00102 -[:INSPECTED_IN]-> DOC-031` during candidate generation.
2. **Supplier Contract Relationship Join Gap**: For Supplier queries (e.g. TC-023 expecting `DOC-006`), `DOC-006` is titled *Spindle Bearing B101 Supply Agreement*. Generic operation manuals occupy candidate pools before contract relationship joins rank `DOC-006` in top-3.
3. **Embedding Semantic Margin**: General-purpose MiniLM dense embeddings exhibit low similarity margin (< 0.05) between procedural maintenance manuals and general machine operation manuals when machine IDs (`M001`, `M008`) overlap.

## 4. Root-Cause Ranking & Bottlenecks
1. **PRIMARY BOTTLENECK**: **Candidate Generation & Graph Relationship Traversal Coverage** — Multi-hop Cypher relationships connecting machines to maintenance defect logs (`M001 -> PO -> DOC-031`) and materials to supplier contracts (`M001 -> MAT-001 -> S001 -> DOC-006`) are not surfacing target documents into initial candidate pools before fusion.
2. **SECONDARY BOTTLENECK**: **Dense Embedding Semantic Resolution** — MiniLM embeddings fail to distinguish procedural maintenance steps from standard machine operation manuals when queries contain machine identifiers (`M001`).
3. **TERTIARY BOTTLENECK**: **Reranking Multi-Feature Score Calibration** — Ranking top-3 displacement occurs when lexical BM25 scores overpower entity relationship joins.

## 5. Official Production Readiness Decision Statement
> **PRODUCTION READINESS: PARTIAL**
>
> *Engineering Rationale*: Phase T established with empirical proof that candidate generation and graph relationship coverage are the primary bottlenecks causing Maintenance Recall@3 (12.5%) and Supplier Recall@3 (30.0%) failures. The platform remains designated **PARTIAL** until Phase U implements targeted candidate generation and graph traversal enhancements.

## 6. Recommended Phase U Strategy
We recommend **Phase U — Relational Candidate Generation & Graph Traversal Engineering**: Extend GraphExpander Cypher candidate generation to execute multi-hop relationship joins (`Machine -> Order/DefectLog -> Procedure` and `Machine -> Material -> Supplier -> ContractDoc`) during initial candidate retrieval, ensuring target documents enter candidate pools prior to reranking.
