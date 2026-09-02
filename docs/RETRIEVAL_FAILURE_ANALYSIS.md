# ContextIQ — Enterprise Retrieval Failure Analysis Report (`docs/RETRIEVAL_FAILURE_ANALYSIS.md`)

## Overview
This document provides a detailed per-question failure breakdown for all test cases in the 30-question evaluation benchmark where the retrieved candidate documents differed from the expected ground-truth document IDs.

---

## 1. Per-Question Failure Matrix

### Test Case TC-001
- **Category**: Maintenance
- **Question**: `"What maintenance procedure applies to machine M001?"`
- **Expected Document IDs**: `['DOC-031']`
- **Retrieved Document IDs (Top 5)**: `['DOC-028', 'DOC-028', 'DOC-028', 'DOC-028', 'DOC-026']`
- **Detected Entities**: `['M001']`
- **BM25 Top Score**: `6.5451` (`DOC-028`)
- **Vector Top Similarity**: `0.7455` (`DOC-026`)
- **RRF Top Score**: `0.0353` (`DOC-028`)
- **Root Cause of Failure**: `DOC-028` is titled *"Welding Robot Operation & Service Manual - M001"* and `DOC-026` is titled *"Plan-to-Produce Quality Standard & Inspection - P001"* (containing `M001` in defect logs). The lexical retriever correctly matched `M001` to `DOC-028` and `DOC-026`, whereas the expected label `DOC-031` is titled *"Plant P003 Batch Audit"* and references machine `M021`.

---

### Test Case TC-002
- **Category**: Maintenance
- **Question**: `"What should an operator check when a machine shows abnormal vibration?"`
- **Expected Document IDs**: `['DOC-033', 'DOC-007']`
- **Retrieved Document IDs (Top 5)**: `['DOC-001', 'DOC-002', 'DOC-003', 'DOC-004', 'DOC-005']`
- **Detected Entities**: `['SN001', 'SN002']`
- **Root Cause of Failure**: General semantic query *"abnormal vibration"* matches multiple machine manuals (`DOC-001` to `DOC-005`) that contain vibration troubleshooting sections, diluting candidates for specific sensor documents `DOC-033` and `DOC-007`.

---

### Test Case TC-003
- **Category**: Maintenance
- **Question**: `"What is the lubrication interval for spindle bearing B101 on M001?"`
- **Expected Document IDs**: `['DOC-006', 'DOC-003']`
- **Retrieved Document IDs (Top 5)**: `['DOC-028', 'DOC-002', 'DOC-023', 'DOC-024', 'DOC-025']`
- **Detected Entities**: `['B101', 'M001']`
- **Root Cause of Failure**: `DOC-028` (Welding Robot Manual M001) dominates lexical scoring due to entity tag `M001`. `DOC-006` contains bearing B101 supplier information, but receives lower BM25 frequency weighting.

---

### Test Case TC-004
- **Category**: Maintenance
- **Question**: `"Which corrective actions are specified for hydraulic pressure drop on M004?"`
- **Expected Document IDs**: `['DOC-004']`
- **Retrieved Document IDs (Top 5)**: `['DOC-005', 'DOC-009', 'DOC-016', 'DOC-004', 'DOC-008']`
- **Detected Entities**: `['M004', 'SN004']`
- **RRF Rank of Expected Document**: **Rank 4** (`DOC-004`)
- **Root Cause of Failure**: `DOC-004` was retrieved in the top-5 candidates at Rank 4, but generic hydraulic pressure terms caused `DOC-005` and `DOC-009` to rank ahead of it.

---

### Test Case TC-005
- **Category**: Maintenance
- **Question**: `"What emergency shutdown steps apply during spindle thermal runaway?"`
- **Expected Document IDs**: `['DOC-005']`
- **Retrieved Document IDs (Top 5)**: `['DOC-028', 'DOC-002', 'DOC-009', 'DOC-005', 'DOC-011']`
- **Detected Entities**: `['M001', 'SN001']`
- **RRF Rank of Expected Document**: **Rank 4** (`DOC-005`)
- **Root Cause of Failure**: Thermal runaway query matched emergency procedures across multiple machine manuals (`DOC-028`, `DOC-002`). `DOC-005` was retrieved at Rank 4.

---

### Test Case TC-006
- **Category**: Maintenance
- **Question**: `"What calibration schedule is mandated for vibration sensor SN001?"`
- **Expected Document IDs**: `['DOC-007', 'DOC-033']`
- **Retrieved Document IDs (Top 5)**: `['DOC-001', 'DOC-002', 'DOC-003', 'DOC-007', 'DOC-033']`
- **Detected Entities**: `['SN001']`
- **RRF Rank of Expected Document**: **Rank 4 & 5** (`DOC-007`, `DOC-033`)
- **Root Cause of Failure**: Both expected documents `DOC-007` and `DOC-033` were retrieved within the top 5 candidates.

---

### Test Case TC-023
- **Category**: Supplier
- **Question**: `"Which supplier and material information is associated with replacement parts for M001?"`
- **Expected Document IDs**: `['DOC-006']`
- **Retrieved Document IDs (Top 5)**: `['DOC-028', 'DOC-028', 'DOC-026', 'DOC-028', 'DOC-028']`
- **Detected Entities**: `['M001', 'S001', 'MAT-001']`
- **Root Cause of Failure**: High term frequency of `M001` in `DOC-028` manual causes `DOC-028` section chunks to occupy the top candidate slots, pushing supplier agreement `DOC-006` below rank 5.

---

## 2. Summary of Core Retrieval Failure Patterns

1. **Entity Dominance Bias**: When a specific entity code (e.g. `M001`) appears frequently in a dedicated machine manual (`DOC-028`), BM25 lexical search returns multiple section chunks from that manual, displacing secondary documents (like supplier agreements or quality standards).
2. **Generic Technical Term Overlap**: Terms like *"vibration"*, *"hydraulic pressure"*, *"thermal runaway"*, and *"calibration"* appear across multiple machine manuals, diluting vector search similarity scores.
3. **Chunk Deduplication vs Rank Depth**: Top-5 retrieval returns multiple section chunks from the same primary document (`DOC-028_CHUNK_01`, `DOC-028_CHUNK_02`, `DOC-028_CHUNK_03`), limiting document diversity in the top-5 window.
