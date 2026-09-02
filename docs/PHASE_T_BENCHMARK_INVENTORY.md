# ContextIQ — Phase T Benchmark Inventory (`docs/PHASE_T_BENCHMARK_INVENTORY.md`)

## Complete 30-Query Benchmark Inventory

| Query ID | Category | Query | Expected Docs | Expected Chunks | Expected Entities | Supported/Unsupported |
|---|---|---|---|---|---|---|
| **TC-001** | Maintenance | *"What maintenance procedure applies to machine M001?"* | `DOC-031` | `DOC-031_CHUNK_01, DOC-031_CHUNK_02, DOC-031_CHUNK_03...` | `M001, P003` | Supported |
| **TC-002** | Maintenance | *"What should an operator check when a machine shows abnormal vibration?"* | `DOC-033, DOC-007` | `DOC-033_CHUNK_01, DOC-033_CHUNK_02, DOC-033_CHUNK_03...` | `SN001, SN002` | Supported |
| **TC-003** | Maintenance | *"What is the lubrication interval for spindle bearing B101 on M001?"* | `DOC-006, DOC-003` | `DOC-006_CHUNK_01, DOC-006_CHUNK_02, DOC-006_CHUNK_03...` | `B101, M001` | Supported |
| **TC-004** | Maintenance | *"Which corrective actions are specified for hydraulic pressure drop on M004?"* | `DOC-004` | `DOC-004_CHUNK_01, DOC-004_CHUNK_02, DOC-004_CHUNK_03...` | `M004, SN004` | Supported |
| **TC-005** | Maintenance | *"What emergency shutdown steps apply during spindle thermal runaway?"* | `DOC-005` | `DOC-005_CHUNK_01, DOC-005_CHUNK_02, DOC-005_CHUNK_03...` | `M001, SN001` | Supported |
| **TC-006** | Maintenance | *"What calibration schedule is mandated for vibration sensor SN001?"* | `DOC-007, DOC-033` | `DOC-007_CHUNK_01, DOC-007_CHUNK_02, DOC-007_CHUNK_03...` | `SN001` | Supported |
| **TC-007** | Maintenance | *"What coolant concentration ratio should be maintained for CNC milling machines?"* | `DOC-002` | `DOC-002_CHUNK_01, DOC-002_CHUNK_02, DOC-002_CHUNK_03...` | `M002` | Supported |
| **TC-008** | Maintenance | *"What gear oil specification is required for gearbox GB-200 on M003?"* | `DOC-003` | `DOC-003_CHUNK_01, DOC-003_CHUNK_02, DOC-003_CHUNK_03...` | `M003, GB-200` | Supported |
| **TC-009** | Quality | *"What procedures are relevant to Plan-to-Produce quality inspection at P003?"* | `DOC-031` | `DOC-031_CHUNK_01, DOC-031_CHUNK_02, DOC-031_CHUNK_03...` | `P003` | Supported |
| **TC-010** | Quality | *"What surface roughness tolerance is acceptable for aerospace shaft batch production?"* | `DOC-010` | `DOC-010_CHUNK_01, DOC-010_CHUNK_02, DOC-010_CHUNK_03...` | `MAT-001` | Supported |
| **TC-011** | Quality | *"How are non-conforming parts quarantined during batch inspection at P002?"* | `DOC-011` | `DOC-011_CHUNK_01, DOC-011_CHUNK_02, DOC-011_CHUNK_03...` | `P002` | Supported |
| **TC-012** | Quality | *"What SPC Cpk threshold requires process stoppage at Plant P001?"* | `DOC-012` | `DOC-012_CHUNK_01, DOC-012_CHUNK_02, DOC-012_CHUNK_03...` | `P001` | Supported |
| **TC-013** | Quality | *"What dimensional measurement protocol applies to CMM inspection?"* | `DOC-013` | `DOC-013_CHUNK_01, DOC-013_CHUNK_02, DOC-013_CHUNK_03...` | `CMM-01` | Supported |
| **TC-014** | Quality | *"What is the non-conforming quarantine procedure for defective parts?"* | `DOC-011` | `DOC-011_CHUNK_01, DOC-011_CHUNK_02, DOC-011_CHUNK_03...` | `P002` | Supported |
| **TC-015** | Quality | *"What dimensional measurement protocol applies to CMM coordinate measuring machines?"* | `DOC-013` | `DOC-013_CHUNK_01, DOC-013_CHUNK_02, DOC-013_CHUNK_03...` | `P001` | Supported |
| **TC-016** | Production | *"What is the technical service manual directive for welding robot M008?"* | `DOC-001` | `DOC-001_CHUNK_01, DOC-001_CHUNK_02, DOC-001_CHUNK_03...` | `PO-00102, M008` | Supported |
| **TC-017** | Production | *"What safety protocols are mandatory for automated robotic cell RC-01?"* | `DOC-017` | `DOC-017_CHUNK_01, DOC-017_CHUNK_02, DOC-017_CHUNK_03...` | `RC-01, P002` | Supported |
| **TC-018** | Production | *"How are tool wear offsets recalculated during high-speed milling?"* | `DOC-018` | `DOC-018_CHUNK_01, DOC-018_CHUNK_02, DOC-018_CHUNK_03` | `M001` | Supported |
| **TC-019** | Production | *"What setup checklist must be completed prior to starting production orders?"* | `DOC-019` | `DOC-019_CHUNK_01, DOC-019_CHUNK_02, DOC-019_CHUNK_03...` | `PO-00105` | Supported |
| **TC-020** | Production | *"What OEE performance target is required for Plant P003 assembly line?"* | `DOC-020` | `DOC-020_CHUNK_01, DOC-020_CHUNK_02, DOC-020_CHUNK_03...` | `P003` | Supported |
| **TC-021** | Production | *"What material staging procedure applies to raw steel alloy MAT-001?"* | `DOC-021` | `DOC-021_CHUNK_01, DOC-021_CHUNK_02, DOC-021_CHUNK_03...` | `MAT-001` | Supported |
| **TC-022** | Production | *"What is the operation manual for welding robot M008 at Plant P003?"* | `DOC-001` | `DOC-001_CHUNK_01, DOC-001_CHUNK_02, DOC-001_CHUNK_03...` | `P003, M008` | Supported |
| **TC-023** | Supplier | *"Which supplier and material information is associated with replacement parts for M001?"* | `DOC-006` | `DOC-006_CHUNK_01, DOC-006_CHUNK_02, DOC-006_CHUNK_03...` | `S001, MAT-001, M001` | Supported |
| **TC-024** | Supplier | *"What lead time SLA is guaranteed by Supplier S001 for replacement bearings?"* | `DOC-006, DOC-024` | `DOC-006_CHUNK_01, DOC-006_CHUNK_02, DOC-006_CHUNK_03...` | `S001` | Supported |
| **TC-025** | Supplier | *"What penalty clauses apply to vendor S002 for delayed deliveries?"* | `DOC-025` | `DOC-025_CHUNK_01, DOC-025_CHUNK_02, DOC-025_CHUNK_03...` | `S002` | Supported |
| **TC-026** | Supplier | *"What SLA terms apply to Tier 1 supplier S001 for spare parts?"* | `DOC-006` | `DOC-006_CHUNK_01, DOC-006_CHUNK_02, DOC-006_CHUNK_03...` | `S001` | Supported |
| **TC-027** | Supplier | *"What dual-sourcing strategy applies to critical spindle components?"* | `DOC-027` | `DOC-027_CHUNK_01, DOC-027_CHUNK_02, DOC-027_CHUNK_03...` | `S001, S003` | Supported |
| **TC-028** | EdgeCase | *"What is the vacation policy for employees in the Marketing department?"* | `None (HR/Unsupported)` | `` | `None` | Unsupported |
| **TC-029** | EdgeCase | *"What annual bonus percentage is paid to sales managers at corporate HQ?"* | `None (HR/Unsupported)` | `` | `None` | Unsupported |
| **TC-030** | EdgeCase | *"What quantum computing core cooling protocol is used in the datacenter?"* | `None (HR/Unsupported)` | `` | `None` | Unsupported |
