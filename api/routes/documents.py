"""
ContextIQ — Document Intelligence API Routes
Provides REST endpoints for enterprise document listings, details, chunk browsing, vector similarity search, and collection stats.
"""

from fastapi import APIRouter, Query, HTTPException, Body
from typing import Dict, Any, List, Optional
from documents.service import get_document_service

router = APIRouter()


@router.get("/documents")
async def list_documents() -> List[Dict[str, Any]]:
    """List all ingested enterprise documents with extracted entity counts."""
    service = get_document_service()
    return service.list_documents()


@router.get("/documents/search")
async def search_documents(
    q: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=20),
    plant_id: Optional[str] = Query(None),
    doc_type: Optional[str] = Query(None)
) -> List[Dict[str, Any]]:
    """Perform vector similarity search across ChromaDB document chunks with optional metadata filters."""
    service = get_document_service()
    return service.search_vector_store(query=q, top_k=top_k, plant_id=plant_id, doc_type=doc_type)


@router.get("/documents/{document_id}")
async def get_document_detail(document_id: str) -> Dict[str, Any]:
    """Retrieve details, metadata, and extracted entities for a single document."""
    service = get_document_service()
    doc = service.get_document_details(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")
    return doc


@router.get("/documents/{document_id}/chunks")
async def get_document_chunks(document_id: str) -> List[Dict[str, Any]]:
    """Retrieve semantic section chunks for a document."""
    service = get_document_service()
    doc = service.get_document_details(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")
    return doc.get("chunks", [])


@router.get("/vector/stats")
async def get_vector_stats() -> Dict[str, Any]:
    """Return ChromaDB vector collection statistics."""
    service = get_document_service()
    return service.vector_store.get_stats()


@router.post("/vector/search")
async def vector_search_post(payload: Dict[str, Any] = Body(...)) -> List[Dict[str, Any]]:
    """POST endpoint for vector similarity search."""
    query = payload.get("query", "")
    top_k = payload.get("top_k", 5)
    plant_id = payload.get("plant_id")
    doc_type = payload.get("doc_type")

    service = get_document_service()
    return service.search_vector_store(query=query, top_k=top_k, plant_id=plant_id, doc_type=doc_type)
