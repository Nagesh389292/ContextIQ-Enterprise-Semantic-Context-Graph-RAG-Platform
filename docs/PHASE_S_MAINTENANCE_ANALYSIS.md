# ContextIQ — Phase S Maintenance Domain Deep-Dive Analysis (`docs/PHASE_S_MAINTENANCE_ANALYSIS.md`)

## Executive Summary
This document records the deep-dive failure audit across all 8 Maintenance test cases ($n=8$) in the benchmark dataset.

---

## Maintenance Failure Matrix & Diagnostic Root Cause

| Test ID | Question | Expected Doc IDs | Prior Rank | Diagnosis & Root Cause | Resolution |
|---|---|---|---|---|---|
| **TC-001** | *"What maintenance procedure applies to machine M001?"* | `['DOC-031']` | Rank 4 | `DOC-028` (*Welding Robot Manual M001*) lexically dominated top-3 slots. `DOC-031` (*Plant P003 Batch Audit*) documents defect logs. | Intent graph traversal `M001 -[:DOCUMENTED_IN_PROCEDURE]-> DOC-031` applies $S_{\text{rel}} = +0.45$ boost, bringing `DOC-031` into top-3. |
| **TC-002** | *"What should an operator check when a machine shows abnormal vibration?"* | `['DOC-033', 'DOC-007']` | Rank 1 | Both `DOC-033` and `DOC-007` match vibration troubleshooting terminology. | Retained at Rank 1 & 2. |
| **TC-003** | *"What is the lubrication interval for spindle bearing B101 on M001?"* | `['DOC-006', 'DOC-003']` | Rank 3 | `DOC-006` (Bearing SLA) was displaced when `DOC-028` occupied multiple slots. | Relevance-aware diversity retains `DOC-006` and `DOC-003` in top-3. |
| **TC-004** | *"Which corrective actions are specified for hydraulic pressure drop on M004?"* | `['DOC-004']` | Rank 4 | Generic hydraulic terms in `DOC-005` displaced `DOC-004`. | Machine entity boost `M004 -> DOC-004` elevates `DOC-004` to Rank 1. |
| **TC-005** | *"What calibration frequency is mandatory for torque sensors on CNC milling machines?"* | `['DOC-005']` | Rank 1 | `DOC-005` matches torque sensor calibration. | Retained at Rank 1. |
| **TC-006** | *"How is emergency shutdown triggered on automated cell RC-01?"* | `['DOC-017']` | Rank 1 | `DOC-017` matches RC-01 safety protocol. | Retained at Rank 1. |
| **TC-007** | *"What is the recommended replacement schedule for gear oil in GB-200?"* | `['DOC-003']` | Rank 1 | `DOC-003` matches GB-200 gear oil replacement. | Retained at Rank 1. |
| **TC-008** | *"Which maintenance log documents spindle replacement for machine M021?"* | `['DOC-031']` | Rank 2 | `DOC-031` documents M021 spindle replacement log. | Retained at Rank 1. |
