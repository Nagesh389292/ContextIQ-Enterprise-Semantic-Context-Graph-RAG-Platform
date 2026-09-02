# ContextIQ — Phase T Maintenance Forensic Audit (`docs/PHASE_T_MAINTENANCE_FORENSIC.md`)

## Maintenance Domain Forensic Matrix (Recall@3 = 12.5%)

| Test ID | Question | Expected Docs | Top 10 Candidates | First Failure Stage | Diagnostic Root Cause |
|---|---|---|---|---|---|
| **TC-001** | *"What maintenance procedure applies to machine M001?"* | `DOC-031` | `DOC-028, DOC-028, DOC-028, DOC-028, DOC-026` | **RERANKING** | Candidate pool contained expected docs ['DOC-031'], but final fusion reranker displaced them out of top-10. |
| **TC-002** | *"What should an operator check when a machine shows abnormal vibration?"* | `DOC-033, DOC-007` | `DOC-006, DOC-032, DOC-011, DOC-024, DOC-033` | **GRAPH_EXPANSION** | Graph expansion Cypher traversal failed to reach expected docs ['DOC-033', 'DOC-007'] from entities []. |
| **TC-003** | *"What is the lubrication interval for spindle bearing B101 on M001?"* | `DOC-006, DOC-003` | `DOC-028, DOC-028, DOC-028, DOC-028, DOC-026` | **RERANKING** | Candidate pool contained expected docs ['DOC-006', 'DOC-003'], but final fusion reranker displaced them out of top-10. |
| **TC-004** | *"Which corrective actions are specified for hydraulic pressure drop on M004?"* | `DOC-004` | `DOC-005, DOC-005, DOC-005, DOC-005, DOC-019` | **RERANKING** | Candidate pool contained expected docs ['DOC-004'], but final fusion reranker displaced them out of top-10. |
| **TC-005** | *"What emergency shutdown steps apply during spindle thermal runaway?"* | `DOC-005` | `DOC-009, DOC-037, DOC-016, DOC-032, DOC-023` | **CANDIDATE_GENERATION** | Neither BM25, Vector, nor Graph candidate generators retrieved expected docs ['DOC-005'] into top-10 pools. |
| **TC-006** | *"What calibration schedule is mandated for vibration sensor SN001?"* | `DOC-007, DOC-033` | `DOC-007, DOC-033, DOC-023, DOC-002, DOC-044` | **NONE** | Successfully retrieved expected docs into top-3. |
| **TC-007** | *"What coolant concentration ratio should be maintained for CNC milling machines?"* | `DOC-002` | `DOC-003, DOC-004, DOC-003, DOC-004, DOC-018` | **GRAPH_EXPANSION** | Graph expansion Cypher traversal failed to reach expected docs ['DOC-002'] from entities []. |
| **TC-008** | *"What gear oil specification is required for gearbox GB-200 on M003?"* | `DOC-003` | `DOC-040, DOC-040, DOC-040, DOC-003, DOC-040` | **RANKING_TOP3_DISPLACEMENT** | Expected docs ['DOC-003'] present in top-10 at ranks [4], but fell outside top-3. |
