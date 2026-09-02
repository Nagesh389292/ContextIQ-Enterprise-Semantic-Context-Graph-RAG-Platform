"""
ContextIQ — Context Search API Routes
Exposes GET /api/v1/search and POST /api/v1/search/hybrid for unified Lexical + Vector + Graph-RAG retrieval.
"""

from fastapi import APIRouter, Query, Body, HTTPException
from typing import Dict, Any, List, Optional
from retrieval.hybrid_pipeline import get_hybrid_pipeline

router = APIRouter()


@router.get("", summary="Execute hybrid context search across enterprise documents and knowledge graph")
@router.get("/", summary="Execute hybrid context search across enterprise documents and knowledge graph")
async def execute_search(
    q: str = Query(..., min_length=1, description="Natural language context search query"),
    top_k: int = Query(5, ge=1, le=20, description="Top-k reranked results to return"),
    plant_id: Optional[str] = Query(None, description="Optional Plant facility filter (e.g. P001)"),
    doc_type: Optional[str] = Query(None, description="Optional document type filter (e.g. Maintenance SOP)"),
    expand_graph: bool = Query(True, description="Whether to expand 2-hop Cypher knowledge graph context")
) -> Dict[str, Any]:
    """Execute hybrid BM25 + Vector + RRF reranked search with optional graph expansion."""
    pipeline = get_hybrid_pipeline()
    return pipeline.search(
        query=q, top_k=top_k, plant_id=plant_id, doc_type=doc_type, expand_graph=expand_graph
    )


@router.post("/hybrid", summary="POST endpoint for hybrid retrieval and graph context expansion")
async def execute_hybrid_post(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """POST payload handler for hybrid retrieval."""
    query = payload.get("query") or payload.get("q")
    if not query:
        raise HTTPException(status_code=400, detail="Missing required 'query' parameter.")

    top_k = payload.get("top_k", 5)
    plant_id = payload.get("plant_id")
    doc_type = payload.get("doc_type")
    expand_graph = payload.get("expand_graph", True)

    pipeline = get_hybrid_pipeline()
    return pipeline.search(
        query=query, top_k=top_k, plant_id=plant_id, doc_type=doc_type, expand_graph=expand_graph
    )
