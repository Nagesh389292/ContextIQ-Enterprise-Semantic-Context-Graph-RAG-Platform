"""
Health check routes — verifies connectivity to all services.
"""

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from config import settings

router = APIRouter()


class ServiceStatus(BaseModel):
    status: str  # "ok" | "degraded" | "unavailable"
    latency_ms: float | None = None
    detail: str | None = None


class HealthResponse(BaseModel):
    app: str
    env: str
    timestamp: str
    llm_available: bool
    services: dict[str, ServiceStatus]


class ReadinessResponse(BaseModel):
    status: str  # "READY" | "DEGRADED" | "NOT_READY"
    is_ready: bool
    timestamp: str
    dependencies: dict[str, ServiceStatus]


@router.get("/health", summary="Lightweight health probe")
async def health_check() -> dict:
    """Lightweight liveness probe returning instant status."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.app_env,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/ready", response_model=ReadinessResponse, summary="Comprehensive readiness check")
async def ready_check() -> ReadinessResponse:
    """
    Returns readiness status for all enterprise dependencies:
    PostgreSQL, Neo4j, ChromaDB, and Gemini API.
    """
    import time
    services: dict[str, ServiceStatus] = {}

    # ── PostgreSQL ──────────────────────────────────────────
    try:
        import psycopg2
        t0 = time.perf_counter()
        conn = psycopg2.connect(settings.database_url, connect_timeout=2)
        conn.close()
        services["postgres"] = ServiceStatus(
            status="ok",
            latency_ms=round((time.perf_counter() - t0) * 1000, 2),
        )
    except Exception as exc:
        services["postgres"] = ServiceStatus(
            status="fallback_active", 
            detail=f"SQLite/CSV fallback active ({exc})"
        )

    # ── Neo4j ───────────────────────────────────────────────
    try:
        from neo4j import GraphDatabase
        t0 = time.perf_counter()
        driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )
        driver.verify_connectivity()
        driver.close()
        services["neo4j"] = ServiceStatus(
            status="ok",
            latency_ms=round((time.perf_counter() - t0) * 1000, 2),
        )
    except Exception as exc:
        services["neo4j"] = ServiceStatus(
            status="fallback_active", 
            detail=f"GraphService in-memory fallback active ({exc})"
        )

    # ── ChromaDB ────────────────────────────────────────────
    try:
        import chromadb
        t0 = time.perf_counter()
        client = chromadb.PersistentClient(path=str(settings.chroma_persist_dir))
        _ = client.list_collections()
        services["chromadb"] = ServiceStatus(
            status="ok",
            latency_ms=round((time.perf_counter() - t0) * 1000, 2),
        )
    except Exception as exc:
        services["chromadb"] = ServiceStatus(status="unavailable", detail=str(exc))

    # ── Gemini API ──────────────────────────────────────────
    if settings.is_llm_available:
        services["gemini"] = ServiceStatus(status="ok", detail="Gemini 2.0 Flash active")
    else:
        services["gemini"] = ServiceStatus(
            status="degraded", detail="No API key — Grounded Synthesizer active"
        )

    is_ready = True
    overall_status = "READY"
    if any(s.status == "unavailable" for s in services.values()):
        is_ready = False
        overall_status = "NOT_READY"
    elif any(s.status == "fallback_active" for s in services.values()):
        overall_status = "DEGRADED_READY"

    return ReadinessResponse(
        status=overall_status,
        is_ready=is_ready,
        timestamp=datetime.now(timezone.utc).isoformat(),
        dependencies=services,
    )
