"""
ContextIQ — Reciprocal Rank Fusion (RRF) & Relationship Join Reranker
Fuses and reranks candidates from lexical BM25, vector similarity, and relationship graph candidates.
"""

from typing import Dict, Any, List, Optional, Set


class RRFReranker:
    """Reciprocal Rank Fusion (RRF) & Relationship Join Reranker."""

    def __init__(self, k: int = 60, weight_vector: float = 0.5, weight_lexical: float = 0.5):
        self.k = k
        self.weight_vector = weight_vector
        self.weight_lexical = weight_lexical

    def apply_document_diversity(
        self,
        chunks: List[Dict[str, Any]],
        top_k: int = 5,
        max_per_doc: int = 2
    ) -> List[Dict[str, Any]]:
        """Filter candidates to prevent a single document from dominating top-k slots."""
        doc_counts: Dict[str, int] = {}
        diversified: List[Dict[str, Any]] = []

        for chunk in chunks:
            doc_id = chunk.get("document_id") or chunk.get("metadata", {}).get("document_id")
            if doc_id:
                count = doc_counts.get(doc_id, 0)
                if count >= max_per_doc:
                    continue
                doc_counts[doc_id] = count + 1
            diversified.append(chunk)
            if len(diversified) >= top_k:
                break

        if len(diversified) < top_k:
            seen_ids = set(c["chunk_id"] for c in diversified)
            for chunk in chunks:
                if chunk["chunk_id"] not in seen_ids:
                    diversified.append(chunk)
                    if len(diversified) >= top_k:
                        break

        return diversified

    def apply_relevance_aware_diversity(
        self,
        chunks: List[Dict[str, Any]],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Filter candidates using relevance-aware diversity rather than rigid document caps."""
        if not chunks:
            return []

        selected: List[Dict[str, Any]] = []
        doc_count: Dict[str, int] = {}
        seen_sections: Set[str] = set()

        for chunk in chunks:
            doc_id = chunk.get("document_id", "UNKNOWN")
            section = f"{doc_id}:{chunk.get('section', '')}"
            score = chunk.get("rrf_score", 0.0)

            count = doc_count.get(doc_id, 0)
            if count >= 2:
                # Relevance-Aware Exception: Allow 3rd or 4th chunk if score is high and section is distinct
                if score < 0.45 or section in seen_sections:
                    continue

            if section in seen_sections:
                continue

            selected.append(chunk)
            doc_count[doc_id] = count + 1
            seen_sections.add(section)

            if len(selected) >= top_k:
                break

        # Backfill if necessary
        if len(selected) < top_k:
            for chunk in chunks:
                if chunk not in selected:
                    selected.append(chunk)
                    if len(selected) >= top_k:
                        break

        return selected

    def rerank(
        self,
        bm25_results: List[Dict[str, Any]],
        vector_results: List[Dict[str, Any]],
        entity_results: Optional[List[Dict[str, Any]]] = None,
        graph_target_doc_ids: Optional[List[str]] = None,
        query_intent: str = "semantic",
        query_entities: Optional[List[str]] = None,
        top_k: int = 5,
        apply_diversity: bool = True
    ) -> List[Dict[str, Any]]:
        """Rerank candidates using RRF fusion + normalized multi-feature relationship join scoring."""
        chunk_map: Dict[str, Dict[str, Any]] = {}
        bm25_ranks: Dict[str, int] = {}
        vector_ranks: Dict[str, int] = {}
        entity_ranks: Dict[str, int] = {}

        graph_doc_set = set(graph_target_doc_ids or [])
        q_entities_set = set(query_entities or [])

        for rank, c in enumerate(bm25_results, start=1):
            cid = c["chunk_id"]
            chunk_map[cid] = c
            bm25_ranks[cid] = rank

        for rank, c in enumerate(vector_results, start=1):
            cid = c["chunk_id"]
            if cid not in chunk_map:
                chunk_map[cid] = c
            vector_ranks[cid] = rank

        for rank, c in enumerate(entity_results or [], start=1):
            cid = c["chunk_id"]
            if cid not in chunk_map:
                chunk_map[cid] = c
            entity_ranks[cid] = rank

        fused: List[Dict[str, Any]] = []

        for cid, chunk in chunk_map.items():
            bm25_rank = bm25_ranks.get(cid, 999)
            vec_rank = vector_ranks.get(cid, 999)
            ent_rank = entity_ranks.get(cid, 999)

            # 1. Base RRF Score
            rrf_score = 0.0
            sources = []
            if cid in bm25_ranks:
                rrf_score += 1.0 / (self.k + bm25_rank)
                sources.append("bm25")
            if cid in vector_ranks:
                rrf_score += 1.0 / (self.k + vec_rank)
                sources.append("vector")
            if cid in entity_ranks:
                rrf_score += 1.0 / (self.k + ent_rank)
                sources.append("entity")

            # 2. Normalized Score Signals
            s_bm25 = (1.0 / (1.0 + bm25_rank)) if cid in bm25_ranks else 0.0
            s_vec = (1.0 / (1.0 + vec_rank)) if cid in vector_ranks else 0.0

            # 3. Entity & Relationship Boosts
            doc_id = chunk.get("document_id", "")
            title = chunk.get("document_title", "").lower()
            text = chunk.get("text", "").lower()

            s_entity = 0.0
            if any(e.lower() in text or e.lower() in title for e in q_entities_set):
                s_entity = 0.35

            s_rel = 0.0
            if doc_id in graph_doc_set:
                s_rel = 0.45

            s_intent = 0.0
            # AC-C4 — Entity-Conditional Intent Masking:
            # When the query-understanding layer identified one or more canonical
            # enterprise entities (machines, suppliers, plants, etc.), suppress the
            # generic intent boost for candidates that do not mention any of those
            # entities.  This prevents a broad operational-intent signal from
            # outranking a document that is more specifically tied to the named entity.
            # When no entities were extracted, the intent boost is applied unchanged
            # (identical to the pre-AC-C4 behaviour).
            entity_present_in_query = bool(q_entities_set)
            candidate_contains_entity = any(
                e.lower() in text or e.lower() in title
                for e in q_entities_set
            ) if entity_present_in_query else True  # vacuously true → no masking

            if candidate_contains_entity:
                if query_intent == "maintenance" and any(k in title or k in text for k in ["maintenance", "procedure", "service", "inspection", "audit"]):
                    s_intent = 0.30
                elif query_intent == "supplier" and any(k in title or k in text for k in ["supplier", "contract", "sla", "supply", "agreement"]):
                    s_intent = 0.30
                elif query_intent == "quality" and any(k in title or k in text for k in ["quality", "spc", "cpk", "audit", "non-conforming"]):
                    s_intent = 0.30

            final_score = rrf_score + (0.25 * s_bm25) + (0.25 * s_vec) + s_entity + s_rel + s_intent

            chunk_copy = dict(chunk)
            chunk_copy["rrf_score"] = round(final_score, 6)
            chunk_copy["score"] = round(final_score, 6)
            chunk_copy["matched_sources"] = sources
            fused.append(chunk_copy)

        fused.sort(key=lambda x: x["rrf_score"], reverse=True)

        if apply_diversity:
            return self.apply_relevance_aware_diversity(fused, top_k=top_k)

        return fused[:top_k]
