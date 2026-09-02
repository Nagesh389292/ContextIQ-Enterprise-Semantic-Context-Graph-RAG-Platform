"""
ContextIQ — ReAct Agentic Copilot API Routes
Exposes POST /api/v1/agent/query and POST /api/v1/agent/stream REST endpoints.
"""

from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from agent.router import get_agent_router, ReActAgentRouter

router = APIRouter(prefix="/agent", tags=["ReAct Agentic Copilot"])


class AgentQueryRequest(BaseModel):
    question: str = Field(..., json_schema_extra={"example": "Which supplier provides replacement bearings for machine M001?"})


@router.post("/query")
def query_react_agent(
    payload: AgentQueryRequest,
    router_service: ReActAgentRouter = Depends(get_agent_router)
):
    """Execute ReAct Copilot agent tool routing and return grounded answer with full trace."""
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    return router_service.run_agent(question=payload.question)


@router.post("/stream")
async def stream_react_agent(
    payload: AgentQueryRequest,
    router_service: ReActAgentRouter = Depends(get_agent_router)
):
    """Stream step-by-step agent tool execution trace via Server-Sent Events (SSE)."""
    return StreamingResponse(
        router_service.stream_agent_trace(question=payload.question),
        media_type="text/event-stream"
    )
