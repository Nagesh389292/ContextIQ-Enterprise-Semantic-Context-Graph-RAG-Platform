"""
ContextIQ — Grounded RAG & Copilot API Routes
Exposes POST /api/v1/rag/query and POST /api/v1/rag/stream REST endpoints.
"""

from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from rag.service import get_rag_service, RAGService

router = APIRouter(prefix="/rag", tags=["Grounded RAG & Copilot"])


class RAGQueryRequest(BaseModel):
    question: str = Field(..., json_schema_extra={"example": "What maintenance procedure applies to machine M001?"})
    top_k: int = Field(default=5, ge=1, le=20)
    plant_id: Optional[str] = Field(default=None, json_schema_extra={"example": "P001"})
    doc_type: Optional[str] = Field(default=None, json_schema_extra={"example": "Maintenance SOP"})


class CitationItem(BaseModel):
    citation_id: str
    chunk_id: str
    document_id: str
    document_title: str
    section: str
    snippet: str
    score: float


class RAGQueryResponse(BaseModel):
    question: str
    answer: str
    model: str
    grounding_score: float
    is_grounded: bool
    citations_count: int
    citations: List[CitationItem] = Field(default_factory=list)
    retrieved_chunks_count: int
    entities_extracted: List[str] = Field(default_factory=list)
    graph_triples_expanded: int
    execution_trace: List[Dict[str, Any]] = Field(default_factory=list)


@router.post("/query", response_model=RAGQueryResponse)
def query_grounded_rag(
    payload: RAGQueryRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """Execute full Grounded RAG Generation pipeline with citation auditing."""
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question string cannot be empty.")

    result = rag_service.generate_grounded_answer(
        question=payload.question,
        top_k=payload.top_k,
        plant_id=payload.plant_id,
        doc_type=payload.doc_type
    )
    return result


@router.post("/stream")
async def stream_grounded_rag(
    payload: RAGQueryRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """Stream step-by-step RAG execution trace and answer via Server-Sent Events (SSE)."""
    return StreamingResponse(
        rag_service.stream_rag_trace(question=payload.question),
        media_type="text/event-stream"
    )
