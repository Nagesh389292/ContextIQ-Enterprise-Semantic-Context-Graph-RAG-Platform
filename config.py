"""
ContextIQ — Enterprise Semantic Context Engine
Centralized Configuration using pydantic-settings.
"""

from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────────
    app_name: str = "ContextIQ — Enterprise Semantic Context Engine"
    app_env: str = "development"
    log_level: str = "INFO"

    # ── PostgreSQL ───────────────────────────────────────────
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "esce_db"
    postgres_user: str = "esce_user"
    postgres_password: str = "esce_password"
    database_url: str = (
        "postgresql://esce_user:esce_password@localhost:5432/esce_db"
    )

    # ── Neo4j ────────────────────────────────────────────────
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "esce_neo4j_password"

    # ── LLM ──────────────────────────────────────────────────
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"

    # ── Embeddings ───────────────────────────────────────────
    embedding_provider: str = "sentence-transformers"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    # ── ChromaDB ─────────────────────────────────────────────
    chroma_persist_dir: str = "./data/chroma_db"
    chroma_collection_name: str = "enterprise_docs"

    # ── Ontology ─────────────────────────────────────────────
    ontology_dir: str = "./ontology"
    ontology_namespace: str = "http://enterprise-sce.org/ontology#"

    # ── API & Frontend Server ────────────────────────────────
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_port: int = 5173
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # ── Derived paths (not from env) ─────────────────────────
    @property
    def project_root(self) -> Path:
        return Path(__file__).parent

    @property
    def ontology_path(self) -> Path:
        return self.project_root / "ontology"

    @property
    def data_path(self) -> Path:
        return self.project_root / "data"

    @property
    def documents_path(self) -> Path:
        return self.project_root / "documents"

    @property
    def is_llm_available(self) -> bool:
        return bool(
            self.gemini_api_key
            and self.gemini_api_key.strip()
            and self.gemini_api_key != "your_gemini_api_key_here"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings singleton."""
    return Settings()


# Module-level convenience alias
settings = get_settings()
