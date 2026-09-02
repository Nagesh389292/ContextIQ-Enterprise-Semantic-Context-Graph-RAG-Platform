# ContextIQ — Trust, Governance & Safety Policy

This document outlines the safety guardrails, governance mechanisms, and trust policies built into ContextIQ.

---

## 1. Grounded Generation & Citation Verification

- **100% Citation Requirement**: Every generated answer must explicitly cite document evidence (`DOC-XXX`) from retrieved chunks.
- **Faithfulness Audit**: Synthesized answers are validated by the `GroundingValidator` in `rag/validator.py`. If claims lack direct evidence support in retrieved text, the answer is flagged or rewritten.
- **Benchmark Pass Rate**: 100.00% Groundedness Pass Rate over 30 protected benchmark test cases.

---

## 2. Query Safety & Unsupported Intent Guardrails

- **Unsupported Intent Gating**: Out-of-scope or unanswerable queries (e.g., prompt injections, external political queries, off-topic requests) are classified as `unsupported` by `QueryUnderstandingEngine`.
- **Zero-Citation Fallback**: Unsupported queries safely return an empty response with `provenance.query_intent = "unsupported"` and zero document citations, preventing hallucinated or unsafe responses.

---

## 3. SQL & Cypher Security Guardrails

- **Read-Only Inspection Tools**: Copilot SQL and Cypher query generators run with strict read-only execution permissions.
- **Forbidden Keywords**: Queries containing `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, or `GRANT` are rejected prior to database execution by `AgenticCopilotRouter`.
- **Parameterization**: All graph and relational queries use parameterized inputs to prevent injection attacks.

---

## 4. API Health & Readiness Probes

- **Liveness Probe (`GET /api/v1/health`)**: Instant health check returning service environment and timestamp.
- **Readiness Probe (`GET /api/v1/ready`)**: Deep dependency inspection checking PostgreSQL, Neo4j, ChromaDB, and Gemini API connectivity. Returns `READY`, `DEGRADED_READY`, or `NOT_READY`.

---

## 5. Environment Secrets & Security Hygiene

- **No Hardcoded Credentials**: API keys, passwords, and private URLs are loaded exclusively from environment variables (`.env`).
- **`.gitignore` Enforcement**: `.env`, `.venv`, `node_modules`, `scratch/`, and local vector stores are strictly excluded from git version control.
