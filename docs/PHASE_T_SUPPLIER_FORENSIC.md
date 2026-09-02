# ContextIQ — Phase T Supplier Forensic Audit (`docs/PHASE_T_SUPPLIER_FORENSIC.md`)

## Supplier Domain Forensic Matrix (Recall@3 = 30.0%)

| Test ID | Question | Expected Docs | Top 10 Candidates | First Failure Stage | Diagnostic Root Cause |
|---|---|---|---|---|---|
| **TC-023** | *"Which supplier and material information is associated with replacement parts for M001?"* | `DOC-006` | `DOC-028, DOC-028, DOC-026, DOC-028, DOC-028` | **RANKING_TOP3_DISPLACEMENT** | Expected docs ['DOC-006'] present in top-10 at ranks [9], but fell outside top-3. |
| **TC-024** | *"What lead time SLA is guaranteed by Supplier S001 for replacement bearings?"* | `DOC-006, DOC-024` | `DOC-024, DOC-032, DOC-024, DOC-024, DOC-003` | **NONE** | Successfully retrieved expected docs into top-3. |
| **TC-025** | *"What penalty clauses apply to vendor S002 for delayed deliveries?"* | `DOC-025` | `DOC-027, DOC-027, DOC-025, DOC-043, DOC-027` | **NONE** | Successfully retrieved expected docs into top-3. |
| **TC-026** | *"What SLA terms apply to Tier 1 supplier S001 for spare parts?"* | `DOC-006` | `DOC-024, DOC-032, DOC-001, DOC-003, DOC-003` | **RERANKING** | Candidate pool contained expected docs ['DOC-006'], but final fusion reranker displaced them out of top-10. |
| **TC-027** | *"What dual-sourcing strategy applies to critical spindle components?"* | `DOC-027` | `DOC-003, DOC-044, DOC-004, DOC-032, DOC-007` | **GRAPH_EXPANSION** | Graph expansion Cypher traversal failed to reach expected docs ['DOC-027'] from entities []. |
