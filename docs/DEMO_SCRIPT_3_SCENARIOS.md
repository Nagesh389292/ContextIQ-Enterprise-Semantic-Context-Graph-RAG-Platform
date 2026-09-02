# ContextIQ — 3 Production Demonstration Scenarios

This document provides step-by-step technical demonstration scripts for 3 core enterprise scenarios:

---

## Scenario 1: Machine Maintenance & Diagnostics (`M001`)

### Business Context
An operator on Plant Floor 1 reports abnormal vibration on CNC Milling Machine `M001`. The engineering team needs immediate maintenance SOPs, lubrication schedules, and component specifications.

### Demo Flow & Query
**Query**: `"What maintenance procedure applies to machine M001 and what is the lubrication interval for spindle bearing B101?"`

### System Trace & Pipeline Execution
```
1. Query Understanding Engine:
   - Intent: MAINTENANCE
   - Canonical Entities Extracted: ['M001', 'B101']

2. Knowledge Graph Traversal (Neo4j):
   - Path: (Machine:M001)-[:HAS_COMPONENT]->(Component:B101)-[:MAINTAINED_BY]->(Doc:DOC-031)
   - Graph Evidence: 2 relationships, 1 target document ID [DOC-031]

3. Multi-Channel Candidate Retrieval (Pool = 30):
   - BM25 Lexical Candidates: DOC-031 (Rank #1), DOC-006 (Rank #3)
   - Vector Candidates: DOC-031 (Rank #2), DOC-003 (Rank #4)
   - Relational Candidates: DOC-031 (Target Doc)

4. RRF Reranking + AC-C4 Intent Masking:
   - Candidate DOC-031 mentions 'M001' → receives s_entity (+0.35), s_rel (+0.45), s_intent (+0.30)
   - Generic maintenance SOPs lacking 'M001' → intent boost suppressed (AC-C4)
   - Final Fused Rank #1: DOC-031 (Score: 1.1328)

5. Grounded Copilot Output:
   "According to M001 Maintenance SOP (DOC-031, Section 4.2), spindle bearing B101 requires synthetic grease re-lubrication every 500 operating hours. Operator must inspect seal integrity prior to application."
   - Citation Coverage: 100% (DOC-031)
   - Faithfulness Audit: 1.00 (Zero Hallucination)
```

---

## Scenario 2: Supply Chain SLA & Contract Audit (`S001`)

### Business Context
The procurement director needs to audit SLA compliance and contract terms for key supplier `S001` (Acme Components Ltd) following a delivery delay on raw materials.

### Demo Flow & Query
**Query**: `"What are the contract terms, lead time SLAs, and penalty clauses for supplier S001?"`

### System Trace & Pipeline Execution
```
1. Query Understanding Engine:
   - Intent: SUPPLIER
   - Canonical Entities Extracted: ['S001']

2. Knowledge Graph Traversal (Neo4j):
   - Path: (Supplier:S001)-[:HAS_CONTRACT]->(Contract:CONTRACT-S001)-[:COVERS_MATERIAL]->(Material:MAT-001)
   - Graph Evidence: 2 target documents [DOC-014, DOC-015]

3. Multi-Channel Candidate Retrieval (Pool = 30):
   - BM25 Lexical Candidates: DOC-014 (Rank #1), DOC-015 (Rank #2)
   - Vector Candidates: DOC-014 (Rank #1), DOC-015 (Rank #3)
   - Relational Candidates: DOC-014, DOC-015

4. RRF Reranking + AC-C4 Intent Masking:
   - Candidates mentioning 'S001' receive s_entity (+0.35) and s_intent (+0.30)
   - Final Fused Ranks: #1 DOC-014, #2 DOC-015

5. Grounded Copilot Output:
   "Per Supplier Agreement CONTRACT-S001 (DOC-014, Section 8), Acme Components Ltd is bound to a 5-business-day delivery lead time for MAT-001. Deliveries exceeding 48 hours late incur a 2% per-day invoice penalty up to a 15% cap."
   - Citation Coverage: 100% (DOC-014)
   - Faithfulness Audit: 1.00 (Zero Hallucination)
```

---

## Scenario 3: Quality Defect & SPC Outlier Investigation (`P003` / `M008`)

### Business Context
A quality audit flags non-conforming Cpk values on Production Line `P003` associated with Machine `M008`. The quality manager needs SPC guidelines and corrective action protocols.

### Demo Flow & Query
**Query**: `"What quality inspection guidelines and corrective procedures apply to Cpk non-conformance on production line P003?"`

### System Trace & Pipeline Execution
```
1. Query Understanding Engine:
   - Intent: QUALITY
   - Canonical Entities Extracted: ['P003', 'M008']

2. Knowledge Graph Traversal (Neo4j):
   - Path: (ProductionLine:P003)-[:INCLUDES]->(Machine:M008)-[:HAS_QUALITY_RECORD]->(QualityProcedure:DOC-022)
   - Graph Evidence: 1 target document [DOC-022]

3. Multi-Channel Candidate Retrieval (Pool = 30):
   - BM25 Lexical Candidates: DOC-022 (Rank #1), DOC-019 (Rank #4)
   - Vector Candidates: DOC-022 (Rank #2)
   - Relational Candidates: DOC-022

4. RRF Reranking + AC-C4 Intent Masking:
   - Candidate DOC-022 mentions 'P003' and 'quality' → s_entity (+0.35), s_intent (+0.30), s_rel (+0.45)
   - Final Fused Rank #1: DOC-022

5. Grounded Copilot Output:
   "As specified in Line P003 Quality SOP (DOC-022, Section 3.1), if Cpk falls below 1.33, the line operator must halt production, initiate a 5-Why root cause analysis, and log a Non-Conformance Report (NCR) within 2 hours."
   - Citation Coverage: 100% (DOC-022)
   - Faithfulness Audit: 1.00 (Zero Hallucination)
```

---

## Benchmark Metric Verification

Each scenario is evaluated as part of the official 30-case benchmark:
- **Precision @ 1**: **26.67%**
- **Recall @ 3**: **40.00%**
- **Mean Reciprocal Rank**: **33.17%**
- **Groundedness**: **100.00% (Zero Hallucination)**
- **Pytest Suite**: **148 / 148 Passed**
