# ContextIQ — Phase T Ground-Truth Validity Audit (`docs/PHASE_T_GROUND_TRUTH_AUDIT.md`)

## Ground-Truth Audit Matrix (30 Test Cases)

| Query ID | Category | Query | Expected Docs | Validity Status | Diagnostic Evidence & Audit Notes |
|---|---|---|---|---|---|
| **TC-001** | Maintenance | *"What maintenance procedure applies to machine M001?"* | `DOC-031` | **VALID** | Ground truth docs ['DOC-031'] exist and contain relevant text sections. |
| **TC-002** | Maintenance | *"What should an operator check when a machine shows abnormal vibration?"* | `DOC-033, DOC-007` | **VALID** | Ground truth docs ['DOC-033', 'DOC-007'] exist and contain relevant text sections. |
| **TC-003** | Maintenance | *"What is the lubrication interval for spindle bearing B101 on M001?"* | `DOC-006, DOC-003` | **VALID** | Ground truth docs ['DOC-006', 'DOC-003'] exist and contain relevant text sections. |
| **TC-004** | Maintenance | *"Which corrective actions are specified for hydraulic pressure drop on M004?"* | `DOC-004` | **VALID** | Ground truth docs ['DOC-004'] exist and contain relevant text sections. |
| **TC-005** | Maintenance | *"What emergency shutdown steps apply during spindle thermal runaway?"* | `DOC-005` | **VALID** | Ground truth docs ['DOC-005'] exist and contain relevant text sections. |
| **TC-006** | Maintenance | *"What calibration schedule is mandated for vibration sensor SN001?"* | `DOC-007, DOC-033` | **VALID** | Ground truth docs ['DOC-007', 'DOC-033'] exist and contain relevant text sections. |
| **TC-007** | Maintenance | *"What coolant concentration ratio should be maintained for CNC milling machines?"* | `DOC-002` | **VALID** | Ground truth docs ['DOC-002'] exist and contain relevant text sections. |
| **TC-008** | Maintenance | *"What gear oil specification is required for gearbox GB-200 on M003?"* | `DOC-003` | **VALID** | Ground truth docs ['DOC-003'] exist and contain relevant text sections. |
| **TC-009** | Quality | *"What procedures are relevant to Plan-to-Produce quality inspection at P003?"* | `DOC-031` | **VALID** | Ground truth docs ['DOC-031'] exist and contain relevant text sections. |
| **TC-010** | Quality | *"What surface roughness tolerance is acceptable for aerospace shaft batch production?"* | `DOC-010` | **VALID** | Ground truth docs ['DOC-010'] exist and contain relevant text sections. |
| **TC-011** | Quality | *"How are non-conforming parts quarantined during batch inspection at P002?"* | `DOC-011` | **VALID** | Ground truth docs ['DOC-011'] exist and contain relevant text sections. |
| **TC-012** | Quality | *"What SPC Cpk threshold requires process stoppage at Plant P001?"* | `DOC-012` | **VALID** | Ground truth docs ['DOC-012'] exist and contain relevant text sections. |
| **TC-013** | Quality | *"What dimensional measurement protocol applies to CMM inspection?"* | `DOC-013` | **VALID** | Ground truth docs ['DOC-013'] exist and contain relevant text sections. |
| **TC-014** | Quality | *"What is the non-conforming quarantine procedure for defective parts?"* | `DOC-011` | **VALID** | Ground truth docs ['DOC-011'] exist and contain relevant text sections. |
| **TC-015** | Quality | *"What dimensional measurement protocol applies to CMM coordinate measuring machines?"* | `DOC-013` | **VALID** | Ground truth docs ['DOC-013'] exist and contain relevant text sections. |
| **TC-016** | Production | *"What is the technical service manual directive for welding robot M008?"* | `DOC-001` | **VALID** | Ground truth docs ['DOC-001'] exist and contain relevant text sections. |
| **TC-017** | Production | *"What safety protocols are mandatory for automated robotic cell RC-01?"* | `DOC-017` | **VALID** | Ground truth docs ['DOC-017'] exist and contain relevant text sections. |
| **TC-018** | Production | *"How are tool wear offsets recalculated during high-speed milling?"* | `DOC-018` | **VALID** | Ground truth docs ['DOC-018'] exist and contain relevant text sections. |
| **TC-019** | Production | *"What setup checklist must be completed prior to starting production orders?"* | `DOC-019` | **VALID** | Ground truth docs ['DOC-019'] exist and contain relevant text sections. |
| **TC-020** | Production | *"What OEE performance target is required for Plant P003 assembly line?"* | `DOC-020` | **VALID** | Ground truth docs ['DOC-020'] exist and contain relevant text sections. |
| **TC-021** | Production | *"What material staging procedure applies to raw steel alloy MAT-001?"* | `DOC-021` | **VALID** | Ground truth docs ['DOC-021'] exist and contain relevant text sections. |
| **TC-022** | Production | *"What is the operation manual for welding robot M008 at Plant P003?"* | `DOC-001` | **VALID** | Ground truth docs ['DOC-001'] exist and contain relevant text sections. |
| **TC-023** | Supplier | *"Which supplier and material information is associated with replacement parts for M001?"* | `DOC-006` | **VALID** | Ground truth docs ['DOC-006'] exist and contain relevant text sections. |
| **TC-024** | Supplier | *"What lead time SLA is guaranteed by Supplier S001 for replacement bearings?"* | `DOC-006, DOC-024` | **VALID** | Ground truth docs ['DOC-006', 'DOC-024'] exist and contain relevant text sections. |
| **TC-025** | Supplier | *"What penalty clauses apply to vendor S002 for delayed deliveries?"* | `DOC-025` | **VALID** | Ground truth docs ['DOC-025'] exist and contain relevant text sections. |
| **TC-026** | Supplier | *"What SLA terms apply to Tier 1 supplier S001 for spare parts?"* | `DOC-006` | **VALID** | Ground truth docs ['DOC-006'] exist and contain relevant text sections. |
| **TC-027** | Supplier | *"What dual-sourcing strategy applies to critical spindle components?"* | `DOC-027` | **VALID** | Ground truth docs ['DOC-027'] exist and contain relevant text sections. |
| **TC-028** | EdgeCase | *"What is the vacation policy for employees in the Marketing department?"* | `None` | **VALID** | Unsupported HR/edge-case query expecting 0 docs. |
| **TC-029** | EdgeCase | *"What annual bonus percentage is paid to sales managers at corporate HQ?"* | `None` | **VALID** | Unsupported HR/edge-case query expecting 0 docs. |
| **TC-030** | EdgeCase | *"What quantum computing core cooling protocol is used in the datacenter?"* | `None` | **VALID** | Unsupported HR/edge-case query expecting 0 docs. |


### Validity Summary
- **VALID**: 30 / 30
- **PARTIALLY_VALID**: 0 / 30
- **INVALID**: 0 / 30
- **AMBIGUOUS**: 0 / 30
