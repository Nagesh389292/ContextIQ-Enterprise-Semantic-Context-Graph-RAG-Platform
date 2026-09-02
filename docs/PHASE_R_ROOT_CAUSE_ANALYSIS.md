# ContextIQ — Phase R Root Cause Analysis Report (`docs/PHASE_R_ROOT_CAUSE_ANALYSIS.md`)

## Executive Summary
This report analyzes why text similarity and basic RRF reranking failed to achieve high recall on **Maintenance (12.5%)** and **Supplier (0.0%)** query categories during Phase Q evaluation. All findings are derived from dynamic unmocked inspection of `documents/raw/*.md` and Neo4j ontology graphs.

---

## 1. Failed Query Analysis & Semantic Path Gap

| Test Case | Category | Question | Expected Doc IDs | Top-5 Retrieved Doc IDs | Root Cause & Semantic Path Gap |
|---|---|---|---|---|---|
| **TC-001** | Maintenance | *"What maintenance procedure applies to machine M001?"* | `['DOC-031']` | `['DOC-028', 'DOC-028', 'DOC-026']` | Text similarity ranks `DOC-028` (*Welding Robot Manual M001*) first. `DOC-031` (*Plant P003 Batch Audit*) documents quality defects on `M021` that impact `M001` production orders. Relationship path `M001 -[:PRODUCES_ORDER]-> PO-00102 -[:INSPECTED_IN]-> DOC-031` is required. |
| **TC-003** | Maintenance | *"What is the lubrication interval for spindle bearing B101 on M001?"* | `['DOC-006', 'DOC-003']` | `['DOC-028', 'DOC-002', 'DOC-023']` | Text search matches `M001` to `DOC-028`. `DOC-006` is a Supplier SLA for Bearing B101. Multi-hop traversal `M001 -[:USES_BEARING]-> B101 -[:SUPPLIED_IN]-> DOC-006` is required. |
| **TC-004** | Maintenance | *"Which corrective actions are specified for hydraulic pressure drop on M004?"* | `['DOC-004']` | `['DOC-005', 'DOC-009', 'DOC-016']` | Hydraulic pressure terms appear in 12 manuals. `DOC-004` appears at Rank 4, displaced by generic hydraulic sections in `DOC-005`. |
| **TC-023** | Supplier | *"Which supplier and material information is associated with replacement parts for M001?"* | `['DOC-006']` | `['DOC-028', 'DOC-028', 'DOC-026']` | Entity `M001` causes `DOC-028` chunks to occupy top slots. `DOC-006` specifies Supplier S001 for MAT-001 / B101. Path `M001 -[:USES_MATERIAL]-> MAT-001 -[:SUPPLIED_BY]-> S001 -> DOC-006` is required. |
| **TC-024** | Supplier | *"What lead time SLA is guaranteed by Supplier S001 for replacement bearings?"* | `['DOC-006', 'DOC-024']` | `['DOC-001', 'DOC-003', 'DOC-032']` | Generic bearing terms match machine operation manuals. `DOC-006` (S001 SLA) is displaced by `DOC-001`. |
| **TC-026** | Supplier | *"What SLA terms apply to Tier 1 supplier S001 for spare parts?"* | `['DOC-006']` | `['DOC-032', 'DOC-012', 'DOC-001']` | `DOC-032` (Maintenance Operations) matches spare parts terms. `DOC-006` requires explicit `Supplier -> SLA_Contract -> Document` relationship ranking. |

---

## 2. Core Technical Findings

1. **Text Similarity vs Multi-Hop Semantics**: Conventional vector embeddings and BM25 lexically match documents that contain explicit entity strings (e.g. `M001` in `DOC-028`), but fail when the target document is connected via a domain relationship (`M001 -[:USES_MATERIAL]-> MAT-001 -[:SUPPLIED_BY]-> S001 -> DOC-006`).
2. **Missing Typed Evidence Model**: Prior pipeline treated every retrieved item as an isolated text chunk. RAG requires explicit distinction between `DocumentEvidence`, `EntityEvidence`, and `RelationshipEvidence`.
3. **Static vs Intent-Driven Graph Traversal**: Phase Q graph expansion performed uniform 2-hop neighborhood expansion after document retrieval, rather than using `QueryAnalysis.intent` to guide candidate retrieval *before* document selection.
