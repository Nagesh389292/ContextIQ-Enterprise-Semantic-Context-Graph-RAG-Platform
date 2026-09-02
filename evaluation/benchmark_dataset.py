"""
ContextIQ — Evaluation Benchmark Dataset (30 Ground-Truth Q&A Test Cases)
Provides benchmark questions mapped to verified ground-truth documents in documents/raw/.
"""

from typing import List, Dict, Any

BENCHMARK_TEST_CASES: List[Dict[str, Any]] = [
    # ── Maintenance & Reliability (1-8) ──────────────────────
    {
        "id": "TC-001",
        "category": "Maintenance",
        "question": "What maintenance procedure applies to machine M001?",
        "expected_doc_ids": ["DOC-031"],
        "expected_entities": ["M001", "P003"],
        "difficulty": "Easy"
    },
    {
        "id": "TC-002",
        "category": "Maintenance",
        "question": "What should an operator check when a machine shows abnormal vibration?",
        "expected_doc_ids": ["DOC-033", "DOC-007"],
        "expected_entities": ["SN001", "SN002"],
        "difficulty": "Medium"
    },
    {
        "id": "TC-003",
        "category": "Maintenance",
        "question": "What is the lubrication interval for spindle bearing B101 on M001?",
        "expected_doc_ids": ["DOC-006", "DOC-003"],
        "expected_entities": ["B101", "M001"],
        "difficulty": "Easy"
    },
    {
        "id": "TC-004",
        "category": "Maintenance",
        "question": "Which corrective actions are specified for hydraulic pressure drop on M004?",
        "expected_doc_ids": ["DOC-004"],
        "expected_entities": ["M004", "SN004"],
        "difficulty": "Medium"
    },
    {
        "id": "TC-005",
        "category": "Maintenance",
        "question": "What emergency shutdown steps apply during spindle thermal runaway?",
        "expected_doc_ids": ["DOC-005"],
        "expected_entities": ["M001", "SN001"],
        "difficulty": "Hard"
    },
    {
        "id": "TC-006",
        "category": "Maintenance",
        "question": "What calibration schedule is mandated for vibration sensor SN001?",
        "expected_doc_ids": ["DOC-007", "DOC-033"],
        "expected_entities": ["SN001"],
        "difficulty": "Medium"
    },
    {
        "id": "TC-007",
        "category": "Maintenance",
        "question": "What coolant concentration ratio should be maintained for CNC milling machines?",
        "expected_doc_ids": ["DOC-002"],
        "expected_entities": ["M002"],
        "difficulty": "Easy"
    },
    {
        "id": "TC-008",
        "category": "Maintenance",
        "question": "What gear oil specification is required for gearbox GB-200 on M003?",
        "expected_doc_ids": ["DOC-003"],
        "expected_entities": ["M003", "GB-200"],
        "difficulty": "Medium"
    },

    # ── Quality Assurance (9-15) ──────────────────────────────
    {
        "id": "TC-009",
        "category": "Quality",
        "question": "What procedures are relevant to Plan-to-Produce quality inspection at P003?",
        "expected_doc_ids": ["DOC-031"],
        "expected_entities": ["P003"],
        "difficulty": "Medium"
    },
    {
        "id": "TC-010",
        "category": "Quality",
        "question": "What surface roughness tolerance is acceptable for aerospace shaft batch production?",
        "expected_doc_ids": ["DOC-010"],
        "expected_entities": ["MAT-001"],
        "difficulty": "Hard"
    },
    {
        "id": "TC-011",
        "category": "Quality",
        "question": "How are non-conforming parts quarantined during batch inspection at P002?",
        "expected_doc_ids": ["DOC-011"],
        "expected_entities": ["P002"],
        "difficulty": "Medium"
    },
    {
        "id": "TC-012",
        "category": "Quality",
        "question": "What SPC Cpk threshold requires process stoppage at Plant P001?",
        "expected_doc_ids": ["DOC-012"],
        "expected_entities": ["P001"],
        "difficulty": "Hard"
    },
    {
        "id": "TC-013",
        "category": "Quality",
        "question": "What dimensional measurement protocol applies to CMM inspection?",
        "expected_doc_ids": ["DOC-013"],
        "expected_entities": ["CMM-01"],
        "difficulty": "Medium"
    },
    {
        "id": "TC-014",
        "category": "Quality",
        "question": "What is the non-conforming quarantine procedure for defective parts?",
        "expected_doc_ids": ["DOC-011"],
        "expected_entities": ["P002"],
        "difficulty": "Easy"
    },
    {
        "id": "TC-015",
        "category": "Quality",
        "question": "What dimensional measurement protocol applies to CMM coordinate measuring machines?",
        "expected_doc_ids": ["DOC-013"],
        "expected_entities": ["P001"],
        "difficulty": "Medium"
    },

    # ── Production & Process (16-22) ──────────────────────────
    {
        "id": "TC-016",
        "category": "Production",
        "question": "What is the technical service manual directive for welding robot M008?",
        "expected_doc_ids": ["DOC-001"],
        "expected_entities": ["PO-00102", "M008"],
        "difficulty": "Easy"
    },
    {
        "id": "TC-017",
        "category": "Production",
        "question": "What safety protocols are mandatory for automated robotic cell RC-01?",
        "expected_doc_ids": ["DOC-017"],
        "expected_entities": ["RC-01", "P002"],
        "difficulty": "Medium"
    },
    {
        "id": "TC-018",
        "category": "Production",
        "question": "How are tool wear offsets recalculated during high-speed milling?",
        "expected_doc_ids": ["DOC-018"],
        "expected_entities": ["M001"],
        "difficulty": "Hard"
    },
    {
        "id": "TC-019",
        "category": "Production",
        "question": "What setup checklist must be completed prior to starting production orders?",
        "expected_doc_ids": ["DOC-019"],
        "expected_entities": ["PO-00105"],
        "difficulty": "Easy"
    },
    {
        "id": "TC-020",
        "category": "Production",
        "question": "What OEE performance target is required for Plant P003 assembly line?",
        "expected_doc_ids": ["DOC-020"],
        "expected_entities": ["P003"],
        "difficulty": "Medium"
    },
    {
        "id": "TC-021",
        "category": "Production",
        "question": "What material staging procedure applies to raw steel alloy MAT-001?",
        "expected_doc_ids": ["DOC-021"],
        "expected_entities": ["MAT-001"],
        "difficulty": "Easy"
    },
    {
        "id": "TC-022",
        "category": "Production",
        "question": "What is the operation manual for welding robot M008 at Plant P003?",
        "expected_doc_ids": ["DOC-001"],
        "expected_entities": ["P003", "M008"],
        "difficulty": "Medium"
    },

    # ── Supplier & Supply Chain (23-27) ───────────────────────
    {
        "id": "TC-023",
        "category": "Supplier",
        "question": "Which supplier and material information is associated with replacement parts for M001?",
        "expected_doc_ids": ["DOC-006"],
        "expected_entities": ["S001", "MAT-001", "M001"],
        "difficulty": "Hard"
    },
    {
        "id": "TC-024",
        "category": "Supplier",
        "question": "What lead time SLA is guaranteed by Supplier S001 for replacement bearings?",
        "expected_doc_ids": ["DOC-006", "DOC-024"],
        "expected_entities": ["S001"],
        "difficulty": "Easy"
    },
    {
        "id": "TC-025",
        "category": "Supplier",
        "question": "What penalty clauses apply to vendor S002 for delayed deliveries?",
        "expected_doc_ids": ["DOC-025"],
        "expected_entities": ["S002"],
        "difficulty": "Medium"
    },
    {
        "id": "TC-026",
        "category": "Supplier",
        "question": "What SLA terms apply to Tier 1 supplier S001 for spare parts?",
        "expected_doc_ids": ["DOC-006"],
        "expected_entities": ["S001"],
        "difficulty": "Hard"
    },
    {
        "id": "TC-027",
        "category": "Supplier",
        "question": "What dual-sourcing strategy applies to critical spindle components?",
        "expected_doc_ids": ["DOC-027"],
        "expected_entities": ["S001", "S003"],
        "difficulty": "Medium"
    },

    # ── Unsupported & HR Edge Cases (28-30) ───────────────────
    {
        "id": "TC-028",
        "category": "EdgeCase",
        "question": "What is the vacation policy for employees in the Marketing department?",
        "expected_doc_ids": [],
        "expected_entities": [],
        "difficulty": "Easy"
    },
    {
        "id": "TC-029",
        "category": "EdgeCase",
        "question": "What annual bonus percentage is paid to sales managers at corporate HQ?",
        "expected_doc_ids": [],
        "expected_entities": [],
        "difficulty": "Easy"
    },
    {
        "id": "TC-030",
        "category": "EdgeCase",
        "question": "What quantum computing core cooling protocol is used in the datacenter?",
        "expected_doc_ids": [],
        "expected_entities": [],
        "difficulty": "Easy"
    }
]
