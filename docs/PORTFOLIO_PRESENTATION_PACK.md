# ContextIQ — Portfolio & Interview Presentation Pack

## 1. 1-Minute Project Elevator Pitch

> "ContextIQ is an enterprise semantic context engine designed to solve retrieval hallucination and vocabulary mismatch in complex domain environments. By unifying structured enterprise data, RDF ontologies, Neo4j knowledge graphs, ChromaDB vector search, and Gemini LLMs, ContextIQ enables multi-hop relational retrieval over manufacturing SOPs, supply contracts, and quality records. 
> 
> Through a disciplined optimization process—including Reciprocal Rank Fusion, candidate pool expansion ($20 \rightarrow 30$), and Entity-Conditional Intent Masking (`AC-C4`)—I improved Top-1 Precision by **+3.34 pp (26.67%)**, Recall@3 by **+6.67 pp (40.00%)**, and MRR by **+2.95 pp (33.17%)** on a 30-case ground-truth benchmark, while maintaining a **100% groundedness pass rate** and a **148-test automated Pytest regression suite**."

---

## 2. 5-Minute Technical Explanation for Architecture Interviews

### Part A: The Problem (Enterprise Knowledge Fragmentation)
Enterprise domain questions (e.g. *"What is the maintenance SOP for CNC machine M001 during hydraulic pressure drop?"*) fail in standard RAG because:
1. Lexical search suffers from vocabulary mismatch (SOP title doesn't explicitly repeat every part number).
2. Vector search lacks structural entity awareness (ranks generic maintenance manuals above machine-specific contracts).
3. Naive LLM generation hallucinates when given noisy or ungrounded evidence.

### Part B: The Solution (Hybrid Graph-RAG Architecture)
ContextIQ solves this through 4 integrated layers:
1. **Semantic Web & Knowledge Graph Layer**: RDF/OWL ontology mapped to Neo4j 5.x graph. Connects machines, components, plants, suppliers, and documents via explicit relationships (`HAS_COMPONENT`, `SUPPLIES`, `GOVERNED_BY`).
2. **Multi-Channel Candidate Retrieval**: Runs 3 parallel candidate generation channels:
   - **BM25 Lexical** ($k=30$)
   - **ChromaDB Vector** (`all-MiniLM-L6-v2`, $k=30$)
   - **Relational Candidate Generator** (Traverses Neo4j graph up to 3 hops for query entities)
3. **RRF Reranking with AC-C4 Entity-Conditional Intent Masking**:
   - Fuses reciprocal ranks ($k=60$) across all 3 channels.
   - **AC-C4 Safeguard**: When canonical entities (e.g. `M001`) are present, generic domain intent boosts (`s_intent`) are suppressed for candidates that lack an entity match.
4. **Grounded Generation & Faithfulness Audit**: Synthesizes responses strictly grounded in top-scoring chunks with 100% citation coverage.

---

## 3. Resume & Portfolio Bullet Points

```text
• Architected ContextIQ, an enterprise semantic context & Graph-RAG platform integrating structured databases, RDF/OWL ontologies, Neo4j knowledge graphs, ChromaDB vector search, and Gemini LLMs.
• Developed Reciprocal Rank Fusion (RRF) reranking with Entity-Conditional Intent Masking (AC-C4) and dynamic candidate pool expansion (20 → 30), lifting Recall@3 by +6.67 pp (40.00%), Precision@1 by +3.34 pp (26.67%), and MRR by +2.95 pp (33.17%) on a 30-case ground-truth benchmark.
• Maintained 100% groundedness pass rate (zero hallucinations) across all test cases and implemented a 148-test automated Pytest regression suite with Docker Compose deployment readiness.
```

---

## 4. Key Metrics Reference Table

| Metric | Initial Baseline | Reconciled Baseline | Final Promoted Baseline | Net Lift |
|---|---:|---:|---:|---:|
| **Precision @ 1** | 13.33% | 23.33% | **26.67%** | **+3.34 pp** |
| **Precision @ 3** | 8.33% | 20.56% | **22.78%** | **+2.22 pp** |
| **Recall @ 3** | 26.67% | 33.33% | **40.00%** | **+6.67 pp** |
| **Recall @ 5** | 26.67% | 45.00% | **46.67%** | **+1.67 pp** |
| **Mean Reciprocal Rank (MRR)** | 24.44% | 30.22% | **33.17%** | **+2.95 pp** |
| **Groundedness Pass Rate** | 100.00% | 100.00% | **100.00%** | **0.00 pp** |
| **Pytest Backend Tests** | 143 passed | 143 passed | **148 / 148 Passed** | **+5 New Tests** |
