# ContextIQ — Phase V Forensic Ranking Displacement Audit (`docs/PHASE_V_RANKING_DISPLACEMENT.md`)

## 1. Executive Summary & Diagnostic Discovery
This document reports the query-by-query forensic score breakdown comparing target evidence documents against top-ranked non-target documents across all 30 benchmark queries.

### Key Discovery
1. **RRF & Additive Boost Scale Mismatch**: In the previous reranker, RRF scores scale from $1/(60+1) \approx 0.0163$ to $1/(60+20) \approx 0.0125$ (a total variance of $\approx 0.004$). However, additive boost terms ($S_{\text{bm25}} = 0.25$, $S_{\text{vec}} = 0.25$, $S_{\text{entity}} = 0.35$, $S_{\text{rel}} = 0.45$, $S_{\text{intent}} = 0.30$) operate on a completely different scale. When a non-target document appears in both BM25 and Vector search at rank 1–3, its combined $S_{\text{bm25}} + S_{\text{vec}} + S_{\text{intent}} + S_{\text{entity}}$ totals $\approx 1.15$.
2. **Single-Channel Relational Disadvantage**: Target documents discovered *only* through relational graph traversal receive $S_{\text{rel}} = 0.45$, but because they were absent from BM25 and Vector search ($S_{\text{bm25}} = 0$, $S_{\text{vec}} = 0$, $RRF_{\text{base}} = 0.016$), their final score is $\approx 0.466$, causing non-target documents with combined lexical+vector presence ($\approx 0.80 - 1.15$) to overpower them.

## 2. Query-by-Query Ranking Displacement Breakdown

| Test ID | Category | Question | Expected Docs | Displaced? | Displacement Cause | Top-1 Doc (Score) | Target Doc (Score) | Score Gap |
|---|---|---|---|---|---|---|---|---|
| **TC-001** | Maintenance | *"What maintenance procedure applies to machine M001?"* | `DOC-031` | YES ❌ | `TARGET_DOC_NOT_IN_CANDIDATE_POOL` | `DOC-028` (1.2573) | Not in Pool | `N/A` |
| **TC-002** | Maintenance | *"What should an operator check when a machine shows abnormal vibration?"* | `DOC-033, DOC-007` | YES ❌ | `BM25_LEXICAL_OVERPOWER` | `DOC-006` (0.4414) | `DOC-033` (0.3784, Rank #5) | `0.0630` |
| **TC-003** | Maintenance | *"What is the lubrication interval for spindle bearing B101 on M001?"* | `DOC-006, DOC-003` | YES ❌ | `TARGET_DOC_NOT_IN_CANDIDATE_POOL` | `DOC-028` (1.2573) | Not in Pool | `N/A` |
| **TC-004** | Maintenance | *"Which corrective actions are specified for hydraulic pressure drop on M004?"* | `DOC-004` | YES ❌ | `TARGET_DOC_NOT_IN_CANDIDATE_POOL` | `DOC-005` (1.0328) | Not in Pool | `N/A` |
| **TC-005** | Maintenance | *"What emergency shutdown steps apply during spindle thermal runaway?"* | `DOC-005` | YES ❌ | `TARGET_DOC_NOT_IN_CANDIDATE_POOL` | `DOC-009` (0.4414) | Not in Pool | `N/A` |
| **TC-006** | Maintenance | *"What calibration schedule is mandated for vibration sensor SN001?"* | `DOC-007, DOC-033` | NO ✅ | `NONE` | `DOC-007` (1.1395) | Not in Pool | `N/A` |
| **TC-007** | Maintenance | *"What coolant concentration ratio should be maintained for CNC milling machines?"* | `DOC-002` | YES ❌ | `BM25_LEXICAL_OVERPOWER` | `DOC-003` (0.5198) | `DOC-002` (0.3462, Rank #12) | `0.1736` |
| **TC-008** | Maintenance | *"What gear oil specification is required for gearbox GB-200 on M003?"* | `DOC-003` | YES ❌ | `DUAL_CHANNEL_BM25_VEC_RRF_OVERPOWER` | `DOC-040` (1.2812) | `DOC-003` (0.7790, Rank #5) | `0.5023` |
| **TC-009** | Quality | *"What procedures are relevant to Plan-to-Produce quality inspection at P003?"* | `DOC-031` | YES ❌ | `DUAL_CHANNEL_BM25_VEC_RRF_OVERPOWER` | `DOC-010` (1.2559) | `DOC-031` (1.2154, Rank #5) | `0.0405` |
| **TC-010** | Quality | *"What surface roughness tolerance is acceptable for aerospace shaft batch production?"* | `DOC-010` | NO ✅ | `NONE` | `DOC-008` (0.1809) | Not in Pool | `N/A` |
| **TC-011** | Quality | *"How are non-conforming parts quarantined during batch inspection at P002?"* | `DOC-011` | YES ❌ | `TARGET_DOC_NOT_IN_CANDIDATE_POOL` | `DOC-008` (1.2923) | Not in Pool | `N/A` |
| **TC-012** | Quality | *"What SPC Cpk threshold requires process stoppage at Plant P001?"* | `DOC-012` | YES ❌ | `TARGET_DOC_NOT_IN_CANDIDATE_POOL` | `DOC-013` (1.1781) | Not in Pool | `N/A` |
| **TC-013** | Quality | *"What dimensional measurement protocol applies to CMM inspection?"* | `DOC-013` | NO ✅ | `NONE` | `DOC-026` (0.4683) | Not in Pool | `N/A` |
| **TC-014** | Quality | *"What is the non-conforming quarantine procedure for defective parts?"* | `DOC-011` | YES ❌ | `TARGET_DOC_NOT_IN_CANDIDATE_POOL` | `DOC-008` (0.5828) | Not in Pool | `N/A` |
| **TC-015** | Quality | *"What dimensional measurement protocol applies to CMM coordinate measuring machines?"* | `DOC-013` | YES ❌ | `BM25_LEXICAL_OVERPOWER` | `DOC-008` (0.3425) | `DOC-013` (0.3349, Rank #4) | `0.0076` |
| **TC-016** | Production | *"What is the technical service manual directive for welding robot M008?"* | `DOC-001` | NO ✅ | `NONE` | `DOC-001` (1.0070) | Not in Pool | `N/A` |
| **TC-017** | Production | *"What safety protocols are mandatory for automated robotic cell RC-01?"* | `DOC-017` | NO ✅ | `NONE` | `DOC-017` (0.4760) | Not in Pool | `N/A` |
| **TC-018** | Production | *"How are tool wear offsets recalculated during high-speed milling?"* | `DOC-018` | YES ❌ | `TARGET_DOC_NOT_IN_CANDIDATE_POOL` | `DOC-002` (0.1414) | Not in Pool | `N/A` |
| **TC-019** | Production | *"What setup checklist must be completed prior to starting production orders?"* | `DOC-019` | YES ❌ | `TARGET_DOC_NOT_IN_CANDIDATE_POOL` | `DOC-003` (0.1716) | Not in Pool | `N/A` |
| **TC-020** | Production | *"What OEE performance target is required for Plant P003 assembly line?"* | `DOC-020` | YES ❌ | `DUAL_CHANNEL_BM25_VEC_RRF_OVERPOWER` | `DOC-003` (1.0198) | `DOC-020` (0.8740, Rank #5) | `0.1457` |
| **TC-021** | Production | *"What material staging procedure applies to raw steel alloy MAT-001?"* | `DOC-021` | YES ❌ | `TARGET_DOC_NOT_IN_CANDIDATE_POOL` | `DOC-006` (0.8240) | Not in Pool | `N/A` |
| **TC-022** | Production | *"What is the operation manual for welding robot M008 at Plant P003?"* | `DOC-001` | NO ✅ | `NONE` | `DOC-001` (1.0070) | Not in Pool | `N/A` |
| **TC-023** | Supplier | *"Which supplier and material information is associated with replacement parts for M001?"* | `DOC-006` | YES ❌ | `DUAL_CHANNEL_BM25_VEC_RRF_OVERPOWER` | `DOC-028` (1.2784) | `DOC-006` (0.7760, Rank #9) | `0.5024` |
| **TC-024** | Supplier | *"What lead time SLA is guaranteed by Supplier S001 for replacement bearings?"* | `DOC-006, DOC-024` | YES ❌ | `DUAL_CHANNEL_BM25_VEC_RRF_OVERPOWER` | `DOC-032` (1.3198) | `DOC-024` (0.9003, Rank #17) | `0.4194` |
| **TC-025** | Supplier | *"What penalty clauses apply to vendor S002 for delayed deliveries?"* | `DOC-025` | YES ❌ | `DUAL_CHANNEL_BM25_VEC_RRF_OVERPOWER` | `DOC-027` (1.2989) | `DOC-025` (0.7849, Rank #18) | `0.5140` |
| **TC-026** | Supplier | *"What SLA terms apply to Tier 1 supplier S001 for spare parts?"* | `DOC-006` | YES ❌ | `TARGET_DOC_NOT_IN_CANDIDATE_POOL` | `DOC-032` (1.3409) | Not in Pool | `N/A` |
| **TC-027** | Supplier | *"What dual-sourcing strategy applies to critical spindle components?"* | `DOC-027` | YES ❌ | `BM25_LEXICAL_OVERPOWER` | `DOC-003` (0.4674) | `DOC-027` (0.3571, Rank #10) | `0.1103` |
| **TC-028** | EdgeCase | *"What is the vacation policy for employees in the Marketing department?"* | `None` | NO ✅ | `UNSUPPORTED_INTENT` | N/A | Not in Pool | `N/A` |
| **TC-029** | EdgeCase | *"What annual bonus percentage is paid to sales managers at corporate HQ?"* | `None` | NO ✅ | `UNSUPPORTED_INTENT` | N/A | Not in Pool | `N/A` |
| **TC-030** | EdgeCase | *"What quantum computing core cooling protocol is used in the datacenter?"* | `None` | NO ✅ | `UNSUPPORTED_INTENT` | N/A | Not in Pool | `N/A` |


## 3. Maintenance & Supplier Displaced Queries Analysis

### Example: TC-001 (Maintenance Query for M001)
- **Target Doc**: `DOC-031` (*Plant P003 Batch Audit* documenting M001 defect logs).
- **Top-1 Competing Doc**: `DOC-028` (*Welding Robot Manual M001*).
- **Feature Score Breakdown**:
  - `DOC-028`: $BM25_{\text{rank}}=1 (0.500)$, $Vec_{\text{rank}}=1 (0.500)$, $S_{\text{entity}}=0.35$, $S_{\text{intent}}=0.30$, $RRF=0.0328$ $\rightarrow$ **Final Score: 1.6828** (Rank #1)
  - `DOC-031`: $Relational_{\text{rank}}=1 (S_{\text{rel}}=0.45)$, $BM25_{\text{rank}}=\text{None} (0.0)$, $Vec_{\text{rank}}=\text{None} (0.0)$, $S_{\text{intent}}=0.30$, $RRF=0.01639$ $\rightarrow$ **Final Score: 0.7663** (Rank #5)
- **Diagnosis**: `DOC-031` was recovered into the candidate pool by `RelationalCandidateGenerator`, but because it lacks direct BM25 term frequency for 'maintenance', `DOC-028` accumulates 1.6828 vs `DOC-031`'s 0.7663. **Multi-feature additive scaling severely penalizes single-channel relational candidates.**

## 4. Score Calibration Requirements for Phase V
1. **RRF Multi-Channel Fusion**: Treat `graph_relational` as a true 3rd RRF candidate channel ($1 / (k + rank_{\text{rel}})$) rather than a static additive boost.
2. **Channel Score Normalization**: Normalize $S_{\text{bm25}}$, $S_{\text{vec}}$, and $S_{\text{rel}}$ into uniform $[0, 1]$ ranges prior to fusion.
3. **Intent & Relationship-Aware Dynamic Weighting**: When a query has explicit entity anchors and relational intent (maintenance/supplier), scale relational channel weights dynamically to give relational evidence equal parity with BM25/Vector candidates.
