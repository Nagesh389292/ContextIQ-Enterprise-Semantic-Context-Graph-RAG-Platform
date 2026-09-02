"""
ContextIQ — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from config import settings
from api.routes import health, entities, graph, documents, rag, search, evaluation, governance, agent

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description=(
            "ContextIQ — Semantic Enterprise Intelligence Engine combining "
            "ontology-driven semantic modeling, knowledge graphs, vector search, and LLM-based RAG."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── CORS ────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows React dev server on 5173
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ─────────────────────────────────────────────
    app.include_router(health.router, prefix="/api/v1", tags=["System Health"])
    app.include_router(entities.router, prefix="/api/v1/entities", tags=["Entities"])
    app.include_router(graph.router, prefix="/api/v1/graph", tags=["Knowledge Graph"])
    app.include_router(documents.router, prefix="/api/v1", tags=["Document Intelligence"])
    app.include_router(rag.router, prefix="/api/v1", tags=["RAG & Copilot"])
    app.include_router(search.router, prefix="/api/v1/search", tags=["Context Search"])
    app.include_router(evaluation.router, prefix="/api/v1/evaluation", tags=["Evaluation"])
    app.include_router(governance.router, prefix="/api/v1", tags=["Data Quality & SHACL Governance"])
    app.include_router(agent.router, prefix="/api/v1", tags=["ReAct Agentic Copilot"])

    # ── Startup / Shutdown ──────────────────────────────────
    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Starting {settings.app_name} [{settings.app_env}]")
        logger.info(f"LLM available: {settings.is_llm_available} (Model: {settings.gemini_model})")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down ContextIQ API")

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.app_env == "development",
        log_level=settings.log_level.lower(),
    )
