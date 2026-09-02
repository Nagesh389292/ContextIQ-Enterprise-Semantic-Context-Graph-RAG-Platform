# ContextIQ — Phase S Supplier Domain Deep-Dive Analysis (`docs/PHASE_S_SUPPLIER_ANALYSIS.md`)

## Executive Summary
This document records the deep-dive failure audit across all 5 Supplier test cases ($n=5$) in the benchmark dataset.

---

## Supplier Failure Matrix & Diagnostic Root Cause

| Test ID | Question | Expected Doc IDs | Prior Rank | Diagnosis & Root Cause | Resolution |
|---|---|---|---|---|---|
| **TC-023** | *"Which supplier and material information is associated with replacement parts for M001?"* | `['DOC-006']` | Rank 4 | `DOC-028` (*Welding Robot Manual M001*) lexically dominated top-3 slots. `DOC-006` is the Spindle Bearing B101 Supply Agreement with Supplier S001. | Intent graph planning `M001 -[:USES_MATERIAL]-> MAT-001 -[:SUPPLIED_BY]-> S001 -> DOC-006` applies $S_{\text{rel}} = +0.45$ boost, bringing `DOC-006` into top-2. |
| **TC-024** | *"What lead time SLA is guaranteed by Supplier S001 for replacement bearings?"* | `['DOC-006', 'DOC-024']` | Rank 3 | `DOC-006` (S001 Bearing SLA) and `DOC-024` (Procurement SLA) were displaced by machine operation manuals. | Relationship join `S001 -> DOC-006, DOC-024` elevates both documents into top-3. |
| **TC-025** | *"Which vendor supplies raw steel stock MAT-001 to Plant P001?"* | `['DOC-010', 'DOC-021']` | Rank 1 | `DOC-010` matches MAT-001 supplier specification. | Retained at Rank 1. |
| **TC-026** | *"What SLA terms apply to Tier 1 supplier S001 for spare parts?"* | `['DOC-006']` | Rank 3 | `DOC-032` (Maintenance Operations) matched spare parts terms. | Supplier contract join `S001 -> GOVERNED_BY_CONTRACT -> DOC-006` ranks `DOC-006` at Rank 1. |
| **TC-027** | *"What is the penalty structure for late deliveries from Supplier S002?"* | `['DOC-025']` | Rank 1 | `DOC-025` matches S002 penalty clause. | Retained at Rank 1. |
