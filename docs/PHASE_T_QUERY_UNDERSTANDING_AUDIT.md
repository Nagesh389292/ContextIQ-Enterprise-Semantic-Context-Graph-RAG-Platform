# ContextIQ — Phase T Query Understanding Audit (`docs/PHASE_T_QUERY_UNDERSTANDING_AUDIT.md`)

## Intent Classification & Entity Extraction Audit

| Test ID | Category | Question | Detected Intent | Detected Entities | Expected Entities | Intent Correct? | Entities Correct? |
|---|---|---|---|---|---|---|---|
| **TC-001** | Maintenance | *"What maintenance procedure applies to machine M001?"* | `maintenance` | `M001` | `M001, P003` | **YES** | **YES** |
| **TC-002** | Maintenance | *"What should an operator check when a machine shows abnormal vibration?"* | `maintenance` | `None` | `SN001, SN002` | **YES** | **NO** |
| **TC-003** | Maintenance | *"What is the lubrication interval for spindle bearing B101 on M001?"* | `maintenance` | `M001` | `B101, M001` | **YES** | **YES** |
| **TC-004** | Maintenance | *"Which corrective actions are specified for hydraulic pressure drop on M004?"* | `maintenance` | `M004` | `M004, SN004` | **YES** | **YES** |
| **TC-005** | Maintenance | *"What emergency shutdown steps apply during spindle thermal runaway?"* | `maintenance` | `None` | `M001, SN001` | **YES** | **NO** |
| **TC-006** | Maintenance | *"What calibration schedule is mandated for vibration sensor SN001?"* | `maintenance` | `SN001` | `SN001` | **YES** | **YES** |
| **TC-007** | Maintenance | *"What coolant concentration ratio should be maintained for CNC milling machines?"* | `maintenance` | `None` | `M002` | **YES** | **NO** |
| **TC-008** | Maintenance | *"What gear oil specification is required for gearbox GB-200 on M003?"* | `maintenance` | `GB-200, M003` | `M003, GB-200` | **YES** | **YES** |
| **TC-009** | Quality | *"What procedures are relevant to Plan-to-Produce quality inspection at P003?"* | `quality` | `P003` | `P003` | **YES** | **YES** |
| **TC-010** | Quality | *"What surface roughness tolerance is acceptable for aerospace shaft batch production?"* | `production` | `None` | `MAT-001` | **NO** | **NO** |
| **TC-011** | Quality | *"How are non-conforming parts quarantined during batch inspection at P002?"* | `quality` | `P002` | `P002` | **YES** | **YES** |
| **TC-012** | Quality | *"What SPC Cpk threshold requires process stoppage at Plant P001?"* | `quality` | `P001` | `P001` | **YES** | **YES** |
| **TC-013** | Quality | *"What dimensional measurement protocol applies to CMM inspection?"* | `quality` | `None` | `CMM-01` | **YES** | **NO** |
| **TC-014** | Quality | *"What is the non-conforming quarantine procedure for defective parts?"* | `quality` | `None` | `P002` | **YES** | **NO** |
| **TC-015** | Quality | *"What dimensional measurement protocol applies to CMM coordinate measuring machines?"* | `quality` | `None` | `P001` | **YES** | **NO** |
| **TC-016** | Production | *"What is the technical service manual directive for welding robot M008?"* | `production` | `M008` | `PO-00102, M008` | **YES** | **YES** |
| **TC-017** | Production | *"What safety protocols are mandatory for automated robotic cell RC-01?"* | `production` | `RC-01` | `RC-01, P002` | **YES** | **YES** |
| **TC-018** | Production | *"How are tool wear offsets recalculated during high-speed milling?"* | `production` | `None` | `M001` | **YES** | **NO** |
| **TC-019** | Production | *"What setup checklist must be completed prior to starting production orders?"* | `production` | `None` | `PO-00105` | **YES** | **NO** |
| **TC-020** | Production | *"What OEE performance target is required for Plant P003 assembly line?"* | `production` | `P003` | `P003` | **YES** | **YES** |
| **TC-021** | Production | *"What material staging procedure applies to raw steel alloy MAT-001?"* | `supplier` | `MAT-001` | `MAT-001` | **NO** | **YES** |
| **TC-022** | Production | *"What is the operation manual for welding robot M008 at Plant P003?"* | `production` | `P003, M008` | `P003, M008` | **YES** | **YES** |
| **TC-023** | Supplier | *"Which supplier and material information is associated with replacement parts for M001?"* | `supplier` | `M001` | `S001, MAT-001, M001` | **YES** | **YES** |
| **TC-024** | Supplier | *"What lead time SLA is guaranteed by Supplier S001 for replacement bearings?"* | `maintenance` | `S001` | `S001` | **NO** | **YES** |
| **TC-025** | Supplier | *"What penalty clauses apply to vendor S002 for delayed deliveries?"* | `supplier` | `S002` | `S002` | **YES** | **YES** |
| **TC-026** | Supplier | *"What SLA terms apply to Tier 1 supplier S001 for spare parts?"* | `supplier` | `S001` | `S001` | **YES** | **YES** |
| **TC-027** | Supplier | *"What dual-sourcing strategy applies to critical spindle components?"* | `maintenance` | `None` | `S001, S003` | **NO** | **NO** |
| **TC-028** | EdgeCase | *"What is the vacation policy for employees in the Marketing department?"* | `unsupported` | `None` | `None` | **YES** | **YES** |
| **TC-029** | EdgeCase | *"What annual bonus percentage is paid to sales managers at corporate HQ?"* | `unsupported` | `None` | `None` | **YES** | **YES** |
| **TC-030** | EdgeCase | *"What quantum computing core cooling protocol is used in the datacenter?"* | `unsupported` | `None` | `None` | **YES** | **YES** |
