# ContextIQ — Phase T Root-Cause Matrix (`docs/PHASE_T_ROOT_CAUSE_MATRIX.md`)

## Comprehensive Diagnostic Root-Cause Matrix (30 Test Cases)

| Test ID | Domain | Expected Docs | Candidate Found? | First Failure Stage | Diagnostic Root Cause | Confidence |
|---|---|---|---|---|---|---|
| **TC-001** | Maintenance | `DOC-031` | **YES** | **RERANKING** | Candidate pool contained expected docs ['DOC-031'], but final fusion reranker displaced them out of top-10. | **HIGH** |
| **TC-002** | Maintenance | `DOC-033, DOC-007` | **YES** | **GRAPH_EXPANSION** | Graph expansion Cypher traversal failed to reach expected docs ['DOC-033', 'DOC-007'] from entities []. | **HIGH** |
| **TC-003** | Maintenance | `DOC-006, DOC-003` | **YES** | **RERANKING** | Candidate pool contained expected docs ['DOC-006', 'DOC-003'], but final fusion reranker displaced them out of top-10. | **HIGH** |
| **TC-004** | Maintenance | `DOC-004` | **YES** | **RERANKING** | Candidate pool contained expected docs ['DOC-004'], but final fusion reranker displaced them out of top-10. | **HIGH** |
| **TC-005** | Maintenance | `DOC-005` | **NO** | **CANDIDATE_GENERATION** | Neither BM25, Vector, nor Graph candidate generators retrieved expected docs ['DOC-005'] into top-10 pools. | **HIGH** |
| **TC-006** | Maintenance | `DOC-007, DOC-033` | **YES** | **NONE** | Successfully retrieved expected docs into top-3. | **HIGH** |
| **TC-007** | Maintenance | `DOC-002` | **YES** | **GRAPH_EXPANSION** | Graph expansion Cypher traversal failed to reach expected docs ['DOC-002'] from entities []. | **HIGH** |
| **TC-008** | Maintenance | `DOC-003` | **YES** | **RANKING_TOP3_DISPLACEMENT** | Expected docs ['DOC-003'] present in top-10 at ranks [4], but fell outside top-3. | **HIGH** |
| **TC-009** | Quality | `DOC-031` | **YES** | **NONE** | Successfully retrieved expected docs into top-3. | **HIGH** |
| **TC-010** | Quality | `DOC-010` | **YES** | **NONE** | Successfully retrieved expected docs into top-3. | **HIGH** |
| **TC-011** | Quality | `DOC-011` | **YES** | **RERANKING** | Candidate pool contained expected docs ['DOC-011'], but final fusion reranker displaced them out of top-10. | **HIGH** |
| **TC-012** | Quality | `DOC-012` | **YES** | **RANKING_TOP3_DISPLACEMENT** | Expected docs ['DOC-012'] present in top-10 at ranks [4], but fell outside top-3. | **HIGH** |
| **TC-013** | Quality | `DOC-013` | **YES** | **NONE** | Successfully retrieved expected docs into top-3. | **HIGH** |
| **TC-014** | Quality | `DOC-011` | **NO** | **CANDIDATE_GENERATION** | Neither BM25, Vector, nor Graph candidate generators retrieved expected docs ['DOC-011'] into top-10 pools. | **HIGH** |
| **TC-015** | Quality | `DOC-013` | **NO** | **CANDIDATE_GENERATION** | Neither BM25, Vector, nor Graph candidate generators retrieved expected docs ['DOC-013'] into top-10 pools. | **HIGH** |
| **TC-016** | Production | `DOC-001` | **YES** | **NONE** | Successfully retrieved expected docs into top-3. | **HIGH** |
| **TC-017** | Production | `DOC-017` | **YES** | **NONE** | Successfully retrieved expected docs into top-3. | **HIGH** |
| **TC-018** | Production | `DOC-018` | **NO** | **CANDIDATE_GENERATION** | Neither BM25, Vector, nor Graph candidate generators retrieved expected docs ['DOC-018'] into top-10 pools. | **HIGH** |
| **TC-019** | Production | `DOC-019` | **NO** | **CANDIDATE_GENERATION** | Neither BM25, Vector, nor Graph candidate generators retrieved expected docs ['DOC-019'] into top-10 pools. | **HIGH** |
| **TC-020** | Production | `DOC-020` | **YES** | **NONE** | Successfully retrieved expected docs into top-3. | **HIGH** |
| **TC-021** | Production | `DOC-021` | **YES** | **RERANKING** | Candidate pool contained expected docs ['DOC-021'], but final fusion reranker displaced them out of top-10. | **HIGH** |
| **TC-022** | Production | `DOC-001` | **YES** | **NONE** | Successfully retrieved expected docs into top-3. | **HIGH** |
| **TC-023** | Supplier | `DOC-006` | **YES** | **RANKING_TOP3_DISPLACEMENT** | Expected docs ['DOC-006'] present in top-10 at ranks [9], but fell outside top-3. | **HIGH** |
| **TC-024** | Supplier | `DOC-006, DOC-024` | **YES** | **NONE** | Successfully retrieved expected docs into top-3. | **HIGH** |
| **TC-025** | Supplier | `DOC-025` | **YES** | **NONE** | Successfully retrieved expected docs into top-3. | **HIGH** |
| **TC-026** | Supplier | `DOC-006` | **YES** | **RERANKING** | Candidate pool contained expected docs ['DOC-006'], but final fusion reranker displaced them out of top-10. | **HIGH** |
| **TC-027** | Supplier | `DOC-027` | **YES** | **GRAPH_EXPANSION** | Graph expansion Cypher traversal failed to reach expected docs ['DOC-027'] from entities []. | **HIGH** |
| **TC-028** | EdgeCase | `None` | **YES** | **NONE** | Unsupported query successfully filtered out. | **HIGH** |
| **TC-029** | EdgeCase | `None` | **YES** | **NONE** | Unsupported query successfully filtered out. | **HIGH** |
| **TC-030** | EdgeCase | `None` | **YES** | **NONE** | Unsupported query successfully filtered out. | **HIGH** |
