# Phase AB — Final Attribution Analysis Report (`docs/PHASE_AB_FINAL.md`)

## Executive Summary

Phase AB completed candidate displacement and reranker attribution analysis across all 30 protected benchmark queries in ContextIQ.

---

## 1. Key Attribution Findings

1. **Fusion Rank Compression (`B_FUSION_DISPLACEMENT`: 40.0%)**:
   - The primary observed cause of performance masking when combining Phase Z fine-tuned embeddings with BM25 is RRF rank reciprocal fusion ($1/(k+r)$), which demotes valid candidates present in one channel (e.g. rank 11–15) if they lack support in the parallel channel.

2. **Candidate Generation Gaps (`A_CANDIDATE_NEVER_GENERATED`: 23.3%)**:
   - 7 queries failed because the target document was missing from initial BM25, Dense, and Relational candidate sets prior to fusion.

3. **Intent Over-Generalization (`E_INTENT_BOOST_DISPLACEMENT`: 13.3%)**:
   - 4 queries failed because generic domain intent boosts favored broad operational guidelines over specific technical manuals.

---

## 2. Verdict & Production Status

- **Phase AB Verdict**: **`PASS / FORENSIC DIAGNOSTIC SUCCESS`**.
- **Production Status**: Production embedder and [`retrieval/reranker.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/retrieval/reranker.py) remain **100% FROZEN & UNTOUCHED**.
- **Verification Integrity**:
  - Pytest Suite: **143 / 143 passed**.
  - Frontend Build: **Clean build, 0 errors**.
