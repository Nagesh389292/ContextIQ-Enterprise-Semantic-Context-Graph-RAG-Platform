# Phase Z — Enterprise Training Data Audit & Hard Negative Mining Report (`docs/PHASE_Z_TRAINING_DATA.md`)

## Executive Summary

Phase Z constructed a domain-specific dataset of **572 contrastive triplets** `(query, positive_evidence, hard_negative)` from the 182 audited enterprise document chunks without consuming or leaking any of the protected 30 benchmark test cases.

---

## 1. Corpus & Triplet Mining Summary

| Metric | Quantity / Percentage | Description |
|---|---:|---|
| **Audited Corpus Chunks** | 182 chunks | Full enterprise corpus (Raw MD manuals, logs, contracts, policies) |
| **Synthetic Template Families** | 12 families | Domain query templates (Maintenance, Supplier, Quality, Production) |
| **Generated Triplets** | **572 triplets** | Mined `(query, positive_evidence, hard_negative)` contrastive pairs |
| **Accepted Hard Negatives** | 572 triplets | Verified non-relevant collision chunks |
| **Rejected Ambiguous Negatives** | 16 triplets | Ambiguous chunks rejected via metadata/entity filtering |
| **False Negative Rejection Rate** | **2.7%** | Strict filtering preventing true positive contamination |
| **Training Split (80%)** | **428 triplets** | 9 query/semantic families |
| **Validation Split (20%)** | **144 triplets** | 3 query/semantic families (100% held-out family split) |

---

## 2. Hard Negative Strategy & Collision Reproduction

Hard negatives were mined to reproduce the exact semantic collision failure patterns identified in Phase Y.1:

1. **Operating Manual vs Maintenance Log**:
   - *Query*: "What specific preventative maintenance procedure applies to machine M001 spindle bearing?"
   - *Positive Evidence*: `DOC-002` (Spindle Maintenance Log for M001)
   - *Hard Negative*: `DOC-003` (Machine Operating Manual mentioning M001) / `DOC-028` (Welding Robot Service Manual)
2. **Robot Service Manual vs Supplier Contract**:
   - *Query*: "What are the commercial contract terms and SLA for supplier S001?"
   - *Positive Evidence*: `DOC-006` (Supplier Contract Agreement)
   - *Hard Negative*: `DOC-028` (Robot Service Manual referencing vendor ID `S012`)
3. **Quality QA Policy vs Machine Defect Analysis**:
   - *Query*: "What defect analysis and root cause log was filed for welding defects on M008?"
   - *Positive Evidence*: `DOC-031` (Defect Analysis Log for M008)
   - *Hard Negative*: `DOC-010` (General Quality Assurance Policy overview)

---

## 3. Train vs Validation Grouped Split

To prevent chunk-level data leakage, triplets were partitioned by **semantic query family**:
- **Training Set (428 triplets)**: Families `Maintenance_M001`, `Maintenance_M002`, `Supplier_S001`, `Supplier_S002`, `Quality_M008`, `Quality_P001`, `Production_P001`, `Production_P003`, `Maintenance_M008`.
- **Validation Set (144 triplets)**: Families `Maintenance_M003`, `Supplier_MAT001`, `Quality_P002`.
