# ContextIQ — Phase U Candidate-Pool Recovery Analysis (`docs/PHASE_U_CANDIDATE_RECOVERY.md`)

## Candidate-Pool Recovery Matrix (30 Test Cases)

| Query ID | Category | Question | Expected Docs | Previously Candidate? | Graph Recovered? | Hop Count | Final Rank | Outcome |
|---|---|---|---|---|---|---|---|---|
| **TC-001** | Maintenance | *"What maintenance procedure applies to machine M001?"* | `DOC-031` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-002** | Maintenance | *"What should an operator check when a machine shows abnormal vibration?"* | `DOC-033, DOC-007` | NO ❌ | YES ✅ | `2` | `5` | **RECOVERED_IN_TOP_10** |
| **TC-003** | Maintenance | *"What is the lubrication interval for spindle bearing B101 on M001?"* | `DOC-006, DOC-003` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-004** | Maintenance | *"Which corrective actions are specified for hydraulic pressure drop on M004?"* | `DOC-004` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-005** | Maintenance | *"What emergency shutdown steps apply during spindle thermal runaway?"* | `DOC-005` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-006** | Maintenance | *"What calibration schedule is mandated for vibration sensor SN001?"* | `DOC-007, DOC-033` | NO ❌ | YES ✅ | `2` | `1` | **RECOVERED_IN_TOP_3** |
| **TC-007** | Maintenance | *"What coolant concentration ratio should be maintained for CNC milling machines?"* | `DOC-002` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-008** | Maintenance | *"What gear oil specification is required for gearbox GB-200 on M003?"* | `DOC-003` | NO ❌ | YES ✅ | `2` | `2` | **RECOVERED_IN_TOP_3** |
| **TC-009** | Quality | *"What procedures are relevant to Plan-to-Produce quality inspection at P003?"* | `DOC-031` | NO ❌ | YES ✅ | `2` | `4` | **RECOVERED_IN_TOP_10** |
| **TC-010** | Quality | *"What surface roughness tolerance is acceptable for aerospace shaft batch production?"* | `DOC-010` | NO ❌ | YES ✅ | `2` | `3` | **RECOVERED_IN_TOP_3** |
| **TC-011** | Quality | *"How are non-conforming parts quarantined during batch inspection at P002?"* | `DOC-011` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-012** | Quality | *"What SPC Cpk threshold requires process stoppage at Plant P001?"* | `DOC-012` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-013** | Quality | *"What dimensional measurement protocol applies to CMM inspection?"* | `DOC-013` | NO ❌ | YES ✅ | `2` | `3` | **RECOVERED_IN_TOP_3** |
| **TC-014** | Quality | *"What is the non-conforming quarantine procedure for defective parts?"* | `DOC-011` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-015** | Quality | *"What dimensional measurement protocol applies to CMM coordinate measuring machines?"* | `DOC-013` | NO ❌ | YES ✅ | `2` | `4` | **RECOVERED_IN_TOP_10** |
| **TC-016** | Production | *"What is the technical service manual directive for welding robot M008?"* | `DOC-001` | NO ❌ | YES ✅ | `2` | `1` | **RECOVERED_IN_TOP_3** |
| **TC-017** | Production | *"What safety protocols are mandatory for automated robotic cell RC-01?"* | `DOC-017` | NO ❌ | YES ✅ | `2` | `1` | **RECOVERED_IN_TOP_3** |
| **TC-018** | Production | *"How are tool wear offsets recalculated during high-speed milling?"* | `DOC-018` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-019** | Production | *"What setup checklist must be completed prior to starting production orders?"* | `DOC-019` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-020** | Production | *"What OEE performance target is required for Plant P003 assembly line?"* | `DOC-020` | NO ❌ | YES ✅ | `2` | `5` | **RECOVERED_IN_TOP_10** |
| **TC-021** | Production | *"What material staging procedure applies to raw steel alloy MAT-001?"* | `DOC-021` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-022** | Production | *"What is the operation manual for welding robot M008 at Plant P003?"* | `DOC-001` | NO ❌ | YES ✅ | `2` | `1` | **RECOVERED_IN_TOP_3** |
| **TC-023** | Supplier | *"Which supplier and material information is associated with replacement parts for M001?"* | `DOC-006` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-024** | Supplier | *"What lead time SLA is guaranteed by Supplier S001 for replacement bearings?"* | `DOC-006, DOC-024` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-025** | Supplier | *"What penalty clauses apply to vendor S002 for delayed deliveries?"* | `DOC-025` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-026** | Supplier | *"What SLA terms apply to Tier 1 supplier S001 for spare parts?"* | `DOC-006` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-027** | Supplier | *"What dual-sourcing strategy applies to critical spindle components?"* | `DOC-027` | NO ❌ | NO ❌ | `0` | `N/A` | **NOT_RECOVERED** |
| **TC-028** | EdgeCase | *"What is the vacation policy for employees in the Marketing department?"* | `None` | YES | YES ✅ | `2` | `N/A` | **RECOVERED_IN_TOP_3** |
| **TC-029** | EdgeCase | *"What annual bonus percentage is paid to sales managers at corporate HQ?"* | `None` | YES | YES ✅ | `2` | `N/A` | **RECOVERED_IN_TOP_3** |
| **TC-030** | EdgeCase | *"What quantum computing core cooling protocol is used in the datacenter?"* | `None` | YES | YES ✅ | `2` | `N/A` | **RECOVERED_IN_TOP_3** |
