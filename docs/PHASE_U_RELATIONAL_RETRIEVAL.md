# ContextIQ — Phase U Relational Candidate Generation & Multi-Hop Graph Traversal (`docs/PHASE_U_RELATIONAL_RETRIEVAL.md`)

## 1. Executive Summary
Phase U designed and implemented targeted relational candidate generation and multi-hop graph traversal in `retrieval/relational_candidates.py`. Document candidates discovered via multi-hop relationship joins are now directly injected into the candidate pool BEFORE reranking.

## 2. Phase T Baseline vs Phase U Comparison

| Metric | Phase T Baseline | Phase U Achieved | Delta |
|---|---:|---:|---:|
| **Precision@1** | 30.0% | **23.3%** | +-6.7% |
| **Precision@3** | 30.0% | **20.6%** | +-9.4% |
| **Recall@3** | 41.7% | **33.3%** | +-8.4% |
| **Recall@5** | 53.3% | **45.0%** | +-8.3% |
| **MRR** | 38.2% | **30.2%** | +-8.0% |
| **Groundedness** | 99.2% | **100.0%** | 0.0% |

## 3. Maintenance & Supplier Deep Dives

### Maintenance Domain Cases (Recall@3 comparison)

| Test ID | Question | Expected Docs | T R@3 | U R@3 | Candidate Recovery Status |
|---|---|---|---|---|---|

### Supplier Domain Cases (Recall@3 comparison)

| Test ID | Question | Expected Docs | T R@3 | U R@3 | Candidate Recovery Status |
|---|---|---|---|---|---|
