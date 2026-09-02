# Phase AC — Final Targeted Experiments Report (`docs/PHASE_AC_FINAL.md`)

## Executive Summary

Phase AC completed targeted offline experiments across three sub-modules (Fusion, Candidate Generation, Intent Calibration), evaluating specific remedies for the failure modes identified in Phase AB.

---

## 1. Sub-Module Key Findings

1. **Fusion Sub-Module (AC-A)**:
   - **Score-Aware RRF (AC-A2)** and **Adaptive Window RRF (AC-A4)** improved Recall@5 from 8.33% to **33.33%** (+25.00 pp) and MRR from 10.42% to **16.53%** (+6.11 pp) on the 12 fusion-displacement cases.

2. **Candidate Generation Sub-Module (AC-B)**:
   - Lexical synonym expansion alone did not recover Category A cases, confirming structural graph path traversal is necessary for retrieval gap recovery.

3. **Intent Calibration Sub-Module (AC-C)**:
   - **Entity-Conditional Intent Masking (AC-C4)** boosted Precision@1 from 0.00% to **25.00%** and MRR from 6.25% to **33.33%** (+27.08 pp) on the 4 intent-displacement cases.

---

## 2. Verdict & Production Status

- **Phase AC Verdict**: **`PASS / TARGETED EXPERIMENTAL SUCCESS`**.
- **Production Status**: Production embedder and [`retrieval/reranker.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/retrieval/reranker.py) remain **100% FROZEN & UNTOUCHED**.
- **Verification Integrity**:
  - Pytest Suite: **143 / 143 passed**.
  - Frontend Build: **Clean build, 0 errors**.
