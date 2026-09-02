# ContextIQ — Technical Case Study: Enterprise Graph-RAG System Optimization

## Executive Summary

Enterprise domain search across manufacturing operations suffers from structural failure modes:
1. **Vocabulary Mismatch**: Equipment codes and part numbers (`M001`, `B101`) rarely co-occur with natural language error descriptions in raw SOP text.
2. **Structural Blindness**: Vector search treats text chunks as isolated vectors, ignoring physical topology (machine $\rightarrow$ subassembly $\rightarrow$ maintenance procedure).
3. **Domain Intent Distortion**: Operational query keywords (`"maintenance"`, `"supplier"`) distort RAG ranking by boosting generic SOPs over entity-specific documents.

**ContextIQ** solves these challenges by combining an RDF/OWL semantic layer, Neo4j knowledge graph, multi-channel hybrid search (BM25 + ChromaDB Vector + Relational Graph), Reciprocal Rank Fusion (RRF), and **Entity-Conditional Intent Masking (`AC-C4`)**.

---

## Technical Problem & Engineering Evolution

```
Baseline Pipeline (Phase U Baseline)
  P@1: 23.33% | R@3: 33.33% | MRR: 30.22%
                    │
                    ▼
Phase AD (AC-C4 Entity-Conditional Masking)
  - Objective: Suppress generic intent boosts for non-entity matching candidates.
  - Result: 5/5 targeted unit tests passed, zero aggregate baseline regression.
                    │
                    ▼
Phase AE-2 (Candidate Pool Expansion 20 → 30)
  - Objective: Recover documents ranked 21–30 previously lost to candidate window truncation.
  - Promoted Metrics: P@1 26.67% (+3.34 pp), R@3 40.00% (+6.67 pp), MRR 33.17% (+2.95 pp)
                    │
                    ▼
Phase AF (Failure Taxonomy Audit & Freeze)
  - Audited all 30 test cases: 5 Rank-1 Perfect Matches, 16 Reranking Displacements, 6 Candidate Gaps, 3 Unsupported.
  - Verified 148/148 Pytest tests, 100% Groundedness, production freeze.
```

---

## Verification & Benchmark Results

All optimization decisions were validated against a protected 30-case ground-truth benchmark and a 148-test Pytest regression suite:

| Metric | Initial Baseline | Reconciled Baseline | **Final Promoted Baseline (Phase AE-2)** | Net Lift |
|---|---:|---:|---:|---:|
| **Precision @ 1** | 13.33% | 23.33% | **26.67%** | **+3.34 pp** |
| **Precision @ 3** | 8.33% | 20.56% | **22.78%** | **+2.22 pp** |
| **Recall @ 3** | 26.67% | 33.33% | **40.00%** | **+6.67 pp** |
| **Recall @ 5** | 26.67% | 45.00% | **46.67%** | **+1.67 pp** |
| **Mean Reciprocal Rank (MRR)** | 24.44% | 30.22% | **33.17%** | **+2.95 pp** |
| **Groundedness Pass Rate** | 100.00% | 100.00% | **100.00%** | **0.00 pp (100% Faithful)** |
| **Backend Test Suite** | 143 passed | 143 passed | **148 / 148 Passed** | **+5 New Tests** |

---

## Known System Limitations (Phase AF Taxonomy Audit)

1. **Candidate-Generation Gaps (6 / 30 cases, 20.0%)**: Target documents absent from top-30 candidate pools due to extreme vocabulary divergence without an explicit graph link. Requires future multi-hop graph expansion.
2. **Reranking Displacements (16 / 30 cases, 53.3%)**: Expected evidence is present in top-30 candidate pool, but competing domain-general SOPs push target document below Rank #1. Managed via relevance-aware diversity.
3. **Unsupported Queries (3 / 30 cases, 10.0%)**: Out-of-domain queries correctly produce zero citations by design to prevent hallucinated answers.
