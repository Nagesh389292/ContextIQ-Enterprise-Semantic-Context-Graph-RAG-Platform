# ContextIQ — Phase T Embedding Quality Audit (`docs/PHASE_T_EMBEDDING_AUDIT.md`)

## Dense Vector Embedding Cosine Similarity Margin Analysis

| Test ID | Category | Question | Max Relevant Sim | Max Irrelevant Sim | Sim Margin | Semantic Weakness? |
|---|---|---|---|---|---|---|
| **TC-001** | Maintenance | *"What maintenance procedure applies to machine M001?"* | `0.4916` | `0.5233` | `-0.0317` | **YES (Weak Margin)** |
| **TC-002** | Maintenance | *"What should an operator check when a machine shows abnormal vibration?"* | `0.3362` | `0.3303` | `0.006` | **YES (Weak Margin)** |
| **TC-003** | Maintenance | *"What is the lubrication interval for spindle bearing B101 on M001?"* | `0.3504` | `0.579` | `-0.2286` | **YES (Weak Margin)** |
| **TC-004** | Maintenance | *"Which corrective actions are specified for hydraulic pressure drop on M004?"* | `0.3698` | `0.3207` | `0.0492` | **YES (Weak Margin)** |
| **TC-005** | Maintenance | *"What emergency shutdown steps apply during spindle thermal runaway?"* | `0.2709` | `0.3373` | `-0.0665` | **YES (Weak Margin)** |
| **TC-006** | Maintenance | *"What calibration schedule is mandated for vibration sensor SN001?"* | `0.4846` | `0.4015` | `0.083` | **NO (Strong Margin)** |
| **TC-007** | Maintenance | *"What coolant concentration ratio should be maintained for CNC milling machines?"* | `0.2582` | `0.2745` | `-0.0164` | **YES (Weak Margin)** |
| **TC-008** | Maintenance | *"What gear oil specification is required for gearbox GB-200 on M003?"* | `0.3802` | `0.3586` | `0.0216` | **YES (Weak Margin)** |
| **TC-009** | Quality | *"What procedures are relevant to Plan-to-Produce quality inspection at P003?"* | `0.7408` | `0.3935` | `0.3473` | **NO (Strong Margin)** |
| **TC-010** | Quality | *"What surface roughness tolerance is acceptable for aerospace shaft batch production?"* | `0.502` | `0.331` | `0.171` | **NO (Strong Margin)** |
| **TC-011** | Quality | *"How are non-conforming parts quarantined during batch inspection at P002?"* | `0.3788` | `0.3699` | `0.0089` | **YES (Weak Margin)** |
| **TC-012** | Quality | *"What SPC Cpk threshold requires process stoppage at Plant P001?"* | `0.4508` | `0.3468` | `0.1039` | **NO (Strong Margin)** |
| **TC-013** | Quality | *"What dimensional measurement protocol applies to CMM inspection?"* | `0.4622` | `0.2891` | `0.1731` | **NO (Strong Margin)** |
| **TC-014** | Quality | *"What is the non-conforming quarantine procedure for defective parts?"* | `0.2404` | `0.3638` | `-0.1234` | **YES (Weak Margin)** |
| **TC-015** | Quality | *"What dimensional measurement protocol applies to CMM coordinate measuring machines?"* | `0.2506` | `0.2178` | `0.0328` | **YES (Weak Margin)** |
| **TC-016** | Production | *"What is the technical service manual directive for welding robot M008?"* | `0.7586` | `0.4807` | `0.2779` | **NO (Strong Margin)** |
| **TC-017** | Production | *"What safety protocols are mandatory for automated robotic cell RC-01?"* | `0.2569` | `0.391` | `-0.1341` | **YES (Weak Margin)** |
| **TC-018** | Production | *"How are tool wear offsets recalculated during high-speed milling?"* | `0.1846` | `0.2459` | `-0.0613` | **YES (Weak Margin)** |
| **TC-019** | Production | *"What setup checklist must be completed prior to starting production orders?"* | `0.3534` | `0.3028` | `0.0506` | **NO (Strong Margin)** |
| **TC-020** | Production | *"What OEE performance target is required for Plant P003 assembly line?"* | `0.4249` | `0.4247` | `0.0002` | **YES (Weak Margin)** |
| **TC-021** | Production | *"What material staging procedure applies to raw steel alloy MAT-001?"* | `0.3457` | `0.3915` | `-0.0459` | **YES (Weak Margin)** |
| **TC-022** | Production | *"What is the operation manual for welding robot M008 at Plant P003?"* | `0.8328` | `0.5124` | `0.3203` | **NO (Strong Margin)** |
| **TC-023** | Supplier | *"Which supplier and material information is associated with replacement parts for M001?"* | `0.5509` | `0.5584` | `-0.0075` | **YES (Weak Margin)** |
| **TC-024** | Supplier | *"What lead time SLA is guaranteed by Supplier S001 for replacement bearings?"* | `0.4771` | `0.5004` | `-0.0233` | **YES (Weak Margin)** |
| **TC-025** | Supplier | *"What penalty clauses apply to vendor S002 for delayed deliveries?"* | `0.3205` | `0.2736` | `0.0468` | **YES (Weak Margin)** |
| **TC-026** | Supplier | *"What SLA terms apply to Tier 1 supplier S001 for spare parts?"* | `0.3802` | `0.4081` | `-0.0279` | **YES (Weak Margin)** |
| **TC-027** | Supplier | *"What dual-sourcing strategy applies to critical spindle components?"* | `0.26` | `0.2736` | `-0.0136` | **YES (Weak Margin)** |
