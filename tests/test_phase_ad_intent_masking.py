"""
Phase AD Unit Tests — AC-C4 Entity-Conditional Intent Masking.

Tests:
  1. Entity-present query: generic intent boost suppressed for non-entity candidates.
  2. Entity-present query: entity-relevant candidates still receive intent boost.
  3. No-entity query: existing intent behaviour unchanged.
  4. Multiple entities: behaviour is deterministic.
  5. Existing reranker features (s_entity, s_rel, RRF) remain unchanged by AC-C4.
"""
import pytest
from retrieval.reranker import RRFReranker


def make_chunk(chunk_id, doc_id, text, title="", section=""):
    return {
        "chunk_id": chunk_id,
        "document_id": doc_id,
        "document_title": title,
        "text": text,
        "section": section,
        "metadata": {},
    }


@pytest.fixture
def reranker():
    return RRFReranker(k=60)


# ---------------------------------------------------------------------------
# Test 1: Entity-present query — generic intent boost suppressed for
#         candidates that do NOT contain the entity.
# ---------------------------------------------------------------------------
def test_ac_c4_intent_suppressed_for_non_entity_candidate(reranker):
    """
    Query has entity M001 (maintenance intent).
    Candidate A contains M001 → should receive s_intent.
    Candidate B does not contain M001 → s_intent must be suppressed.
    Candidate A should rank above Candidate B despite both matching intent keywords.
    """
    bm25 = [
        make_chunk("B_c1", "DOC-B", "maintenance procedure for general machines", title="General Maintenance SOP"),
        make_chunk("A_c1", "DOC-A", "maintenance procedure for m001 spindle bearing", title="M001 Maintenance Manual"),
    ]
    vec = list(bm25)  # same order

    result = reranker.rerank(
        bm25_results=bm25,
        vector_results=vec,
        query_intent="maintenance",
        query_entities=["M001"],
        top_k=5,
        apply_diversity=False,
    )

    ids = [r["chunk_id"] for r in result]
    assert "A_c1" in ids, "Entity-containing candidate must appear in results"
    assert "B_c1" in ids, "Non-entity candidate must still appear in results"

    a_score = next(r["rrf_score"] for r in result if r["chunk_id"] == "A_c1")
    b_score = next(r["rrf_score"] for r in result if r["chunk_id"] == "B_c1")
    assert a_score > b_score, (
        f"AC-C4: entity-relevant candidate (A, {a_score:.4f}) should outscore "
        f"generic candidate (B, {b_score:.4f}) when entity is present in query"
    )


# ---------------------------------------------------------------------------
# Test 2: Entity-present query — entity-relevant candidate is not suppressed.
# ---------------------------------------------------------------------------
def test_ac_c4_entity_relevant_candidate_receives_intent_boost(reranker):
    """
    Entity candidate containing M001 + intent keyword must score > pure RRF score.
    """
    bm25 = [make_chunk("A_c1", "DOC-A", "maintenance procedure m001", title="M001 Maintenance")]
    vec  = [make_chunk("A_c1", "DOC-A", "maintenance procedure m001", title="M001 Maintenance")]

    # s_intent = 0.30 should be added for A_c1
    result = reranker.rerank(
        bm25_results=bm25,
        vector_results=vec,
        query_intent="maintenance",
        query_entities=["M001"],
        top_k=5,
        apply_diversity=False,
    )

    assert result, "Should return at least one result"
    chunk = result[0]
    # Base RRF score for rank-1 in both lists = 1/(60+1) + 1/(60+1) ≈ 0.0328
    # With s_intent=0.30, final_score > 0.0328
    base_rrf = 2.0 / (60 + 1)
    assert chunk["rrf_score"] > base_rrf + 0.25, (
        f"Entity-relevant candidate should receive intent boost; got {chunk['rrf_score']:.4f}"
    )


# ---------------------------------------------------------------------------
# Test 3: No-entity query — intent behaviour unchanged.
# ---------------------------------------------------------------------------
def test_ac_c4_no_entity_query_intent_behaviour_unchanged(reranker):
    """
    When no entities are in the query, s_intent must be applied as before to
    any candidate matching intent keywords.
    """
    bm25 = [make_chunk("X_c1", "DOC-X", "maintenance inspection procedure", title="Generic Maintenance")]
    vec  = [make_chunk("X_c1", "DOC-X", "maintenance inspection procedure", title="Generic Maintenance")]

    result = reranker.rerank(
        bm25_results=bm25,
        vector_results=vec,
        query_intent="maintenance",
        query_entities=[],   # no entities
        top_k=5,
        apply_diversity=False,
    )

    assert result, "Should return results"
    base_rrf = 2.0 / (60 + 1)
    assert result[0]["rrf_score"] > base_rrf + 0.25, (
        "No-entity query: intent boost should still fire for matching candidate"
    )


# ---------------------------------------------------------------------------
# Test 4: Multiple entities — deterministic behaviour.
# ---------------------------------------------------------------------------
def test_ac_c4_multiple_entities_deterministic(reranker):
    """
    Query with multiple entities [M001, S001].
    Candidate containing S001 should still be boosted (not suppressed).
    """
    bm25 = [
        make_chunk("S_c1", "DOC-S", "supplier contract s001 sla agreement", title="S001 Supplier Contract"),
        make_chunk("G_c1", "DOC-G", "supplier sla agreement general", title="Generic Supplier SLA"),
    ]
    vec = list(bm25)

    result = reranker.rerank(
        bm25_results=bm25,
        vector_results=vec,
        query_intent="supplier",
        query_entities=["M001", "S001"],
        top_k=5,
        apply_diversity=False,
    )

    s_score = next(r["rrf_score"] for r in result if r["chunk_id"] == "S_c1")
    g_score = next(r["rrf_score"] for r in result if r["chunk_id"] == "G_c1")
    assert s_score > g_score, (
        f"Multi-entity query: S001-specific candidate ({s_score:.4f}) should rank "
        f"above generic candidate ({g_score:.4f})"
    )


# ---------------------------------------------------------------------------
# Test 5: s_entity, s_rel, RRF scores are unaffected by AC-C4 change.
# ---------------------------------------------------------------------------
def test_ac_c4_does_not_affect_entity_and_rel_scores(reranker):
    """
    s_entity (entity token in text) and s_rel (graph doc in set) are independent
    of AC-C4. A candidate with a graph relationship should still receive s_rel=0.45
    regardless of whether intent masking applies.
    """
    bm25 = [make_chunk("R_c1", "DOC-R", "report document without keywords")]
    vec  = [make_chunk("R_c1", "DOC-R", "report document without keywords")]

    result = reranker.rerank(
        bm25_results=bm25,
        vector_results=vec,
        entity_results=[],
        graph_target_doc_ids=["DOC-R"],   # graph relationship present
        query_intent="maintenance",
        query_entities=["M001"],           # entity present → intent masked for this candidate
        top_k=5,
        apply_diversity=False,
    )

    assert result, "Should return results"
    chunk = result[0]
    # s_rel = 0.45 should be included even though s_intent is suppressed
    base_rrf = 2.0 / (60 + 1)
    assert chunk["rrf_score"] > base_rrf + 0.40, (
        f"s_rel=0.45 should be preserved; got rrf_score={chunk['rrf_score']:.4f}"
    )
