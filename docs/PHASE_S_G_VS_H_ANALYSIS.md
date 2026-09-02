# ContextIQ — Config G vs Config H Forensic Analysis (`docs/PHASE_S_G_VS_H_ANALYSIS.md`)

## Executive Summary
This document records the forensic query-by-query analysis comparing **Config G** (BM25 + Vector + Entity + Graph without rigid diversity) vs **Config H** (Final Production Pipeline with rigid max-2-chunks diversity).

---

## 1. Forensic Discovery: Why Config H Lowered Recall@5 (86.7% → 68.3%)

1. **Rigid Document Cap Mechanism**: Config H previously enforced `max_per_doc = 2` without checking chunk relevance.
2. **Multi-Document Target Displacements**: For test cases expecting multiple distinct documents (e.g. TC-003 expecting `['DOC-006', 'DOC-003']` and TC-024 expecting `['DOC-006', 'DOC-024']`), `DOC-006` had 4 highly relevant section chunks.
3. **Forced Filler Chunks**: When rigid diversity capped `DOC-006` to 2 chunks, it forced low-relevance filler documents (`DOC-001`, `DOC-012`) into slots 3 and 4, prematurely exhausting top-5 slots and pushing `DOC-003` / `DOC-024` out of top-5!

---

## 2. Redesign: Relevance-Aware Evidence Diversity

Instead of a rigid cap (`max_per_doc = 2`), the reranker now implements **Relevance-Aware Diversity Filtering** (`apply_relevance_aware_diversity`):
- A second or third chunk from the same document is **retained** if its combined normalized score $S_{\text{final}} \ge 0.45$ and its section header provides distinct evidence content.
- Low-scoring duplicate chunks ($S_{\text{final}} < 0.45$) are suppressed to allow lower-ranked distinct documents to surface.
