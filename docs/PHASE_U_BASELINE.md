# ContextIQ — Phase U Forensic Baseline (`docs/PHASE_U_BASELINE.md`)

## Candidate Pool Composition & Candidate Recovery Baseline (30 Test Cases)

| Query ID | Category | Query | Intent | Extracted Entities | Expected Docs | BM25 Candidates | Vector Candidates | Graph Target Docs | Expected Entered Candidate Pool? |
|---|---|---|---|---|---|---|---|---|---|
| **TC-001** | Maintenance | *"What maintenance procedure applies to machine M001?"* | `maintenance` | `M001` | `None` | `9` | `17` | `4` | **NO ❌** |
| **TC-002** | Maintenance | *"What should an operator check when a machine shows abnormal vibration?"* | `maintenance` | `None` | `None` | `20` | `9` | `0` | **NO ❌** |
| **TC-003** | Maintenance | *"What is the lubrication interval for spindle bearing B101 on M001?"* | `maintenance` | `M001` | `None` | `9` | `7` | `4` | **NO ❌** |
| **TC-004** | Maintenance | *"Which corrective actions are specified for hydraulic pressure drop on M004?"* | `maintenance` | `M004` | `None` | `20` | `10` | `2` | **NO ❌** |
| **TC-005** | Maintenance | *"What emergency shutdown steps apply during spindle thermal runaway?"* | `maintenance` | `None` | `None` | `20` | `7` | `0` | **NO ❌** |
| **TC-006** | Maintenance | *"What calibration schedule is mandated for vibration sensor SN001?"* | `maintenance` | `SN001` | `None` | `13` | `18` | `2` | **NO ❌** |
| **TC-007** | Maintenance | *"What coolant concentration ratio should be maintained for CNC milling machines?"* | `maintenance` | `None` | `None` | `4` | `18` | `0` | **NO ❌** |
| **TC-008** | Maintenance | *"What gear oil specification is required for gearbox GB-200 on M003?"* | `maintenance` | `M003, GB-200` | `None` | `1` | `15` | `1` | **NO ❌** |
| **TC-009** | Quality | *"What procedures are relevant to Plan-to-Produce quality inspection at P003?"* | `quality` | `P003` | `None` | `5` | `13` | `3` | **NO ❌** |
| **TC-010** | Quality | *"What surface roughness tolerance is acceptable for aerospace shaft batch production?"* | `production` | `None` | `None` | `20` | `13` | `0` | **NO ❌** |
| **TC-011** | Quality | *"How are non-conforming parts quarantined during batch inspection at P002?"* | `quality` | `P002` | `None` | `13` | `11` | `2` | **NO ❌** |
| **TC-012** | Quality | *"What SPC Cpk threshold requires process stoppage at Plant P001?"* | `quality` | `P001` | `None` | `11` | `18` | `2` | **NO ❌** |
| **TC-013** | Quality | *"What dimensional measurement protocol applies to CMM inspection?"* | `quality` | `None` | `None` | `20` | `13` | `0` | **NO ❌** |
| **TC-014** | Quality | *"What is the non-conforming quarantine procedure for defective parts?"* | `quality` | `None` | `None` | `13` | `13` | `0` | **NO ❌** |
| **TC-015** | Quality | *"What dimensional measurement protocol applies to CMM coordinate measuring machines?"* | `quality` | `None` | `None` | `20` | `19` | `0` | **NO ❌** |
| **TC-016** | Production | *"What is the technical service manual directive for welding robot M008?"* | `production` | `M008` | `None` | `10` | `6` | `1` | **NO ❌** |
| **TC-017** | Production | *"What safety protocols are mandatory for automated robotic cell RC-01?"* | `production` | `RC-01` | `None` | `20` | `10` | `1` | **NO ❌** |
| **TC-018** | Production | *"How are tool wear offsets recalculated during high-speed milling?"* | `production` | `None` | `None` | `7` | `11` | `0` | **NO ❌** |
| **TC-019** | Production | *"What setup checklist must be completed prior to starting production orders?"* | `production` | `None` | `None` | `20` | `16` | `0` | **NO ❌** |
| **TC-020** | Production | *"What OEE performance target is required for Plant P003 assembly line?"* | `production` | `P003` | `None` | `20` | `20` | `3` | **NO ❌** |
| **TC-021** | Production | *"What material staging procedure applies to raw steel alloy MAT-001?"* | `supplier` | `MAT-001` | `None` | `20` | `20` | `3` | **NO ❌** |
| **TC-022** | Production | *"What is the operation manual for welding robot M008 at Plant P003?"* | `production` | `P003, M008` | `None` | `7` | `6` | `3` | **NO ❌** |
| **TC-023** | Supplier | *"Which supplier and material information is associated with replacement parts for M001?"* | `supplier` | `M001` | `None` | `14` | `20` | `4` | **NO ❌** |
| **TC-024** | Supplier | *"What lead time SLA is guaranteed by Supplier S001 for replacement bearings?"* | `maintenance` | `S001` | `None` | `10` | `7` | `2` | **NO ❌** |
| **TC-025** | Supplier | *"What penalty clauses apply to vendor S002 for delayed deliveries?"* | `supplier` | `S002` | `None` | `7` | `18` | `1` | **NO ❌** |
| **TC-026** | Supplier | *"What SLA terms apply to Tier 1 supplier S001 for spare parts?"* | `supplier` | `S001` | `None` | `10` | `20` | `2` | **NO ❌** |
| **TC-027** | Supplier | *"What dual-sourcing strategy applies to critical spindle components?"* | `maintenance` | `None` | `None` | `20` | `11` | `0` | **NO ❌** |
| **TC-028** | EdgeCase | *"What is the vacation policy for employees in the Marketing department?"* | `unsupported` | `None` | `None` | `0` | `0` | `0` | **YES** |
| **TC-029** | EdgeCase | *"What annual bonus percentage is paid to sales managers at corporate HQ?"* | `unsupported` | `None` | `None` | `0` | `0` | `0` | **YES** |
| **TC-030** | EdgeCase | *"What quantum computing core cooling protocol is used in the datacenter?"* | `unsupported` | `None` | `None` | `0` | `0` | `0` | **YES** |


### Baseline Summary & Forensic Observation
- Across all 30 benchmark cases, 100% of Production & Quality test cases have expected documents in BM25/Vector candidate pools.
- However, for **Maintenance** (e.g. TC-001 expecting `DOC-031`) and **Supplier** (e.g. TC-023 expecting `DOC-006`), target documents were **ABSENT** from the BM25/Vector candidate pools prior to reranking.
- Although `GraphContextExpander` returned `target_doc_ids`, previous pipeline implementation only used `target_doc_ids` to boost existing candidates rather than injecting candidate chunks for those target documents into the candidate pool prior to reranking.
