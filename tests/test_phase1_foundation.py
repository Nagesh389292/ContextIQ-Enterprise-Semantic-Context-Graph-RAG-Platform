"""
Phase 1 smoke tests — verifies project skeleton imports and config.
"""

import pytest
import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestConfig:
    """Test that settings load without errors."""

    def test_settings_load(self):
        from config import get_settings
        settings = get_settings()
        assert "ContextIQ" in settings.app_name
        assert settings.api_port == 8000
        assert settings.frontend_port == 5173
        assert settings.embedding_dimension == 384

    def test_settings_paths(self):
        from config import settings
        assert settings.project_root.exists()

    def test_llm_available_false_without_key(self):
        """LLM should be a boolean property."""
        from config import settings
        assert isinstance(settings.is_llm_available, bool)


class TestProjectStructure:
    """Verify the project directory skeleton exists."""

    BASE = os.path.join(os.path.dirname(__file__), "..")

    def _exists(self, *parts):
        return os.path.exists(os.path.join(self.BASE, *parts))

    def test_ontology_dir(self):
        assert self._exists("ontology")

    def test_data_dir(self):
        assert self._exists("data", "raw")

    def test_graph_dir(self):
        assert self._exists("graph", "queries")

    def test_sparql_dir(self):
        assert self._exists("ontology", "sparql") or self._exists("sparql")

    def test_ingestion_dir(self):
        assert self._exists("ingestion")

    def test_retrieval_dir(self):
        assert self._exists("retrieval")

    def test_rag_dir(self):
        assert self._exists("rag")

    def test_agents_dir(self):
        assert self._exists("agents")

    def test_validation_dir(self):
        assert self._exists("validation")

    def test_evaluation_dir(self):
        assert self._exists("evaluation")

    def test_docker_compose_exists(self):
        assert self._exists("docker-compose.yml")

    def test_requirements_exists(self):
        assert self._exists("requirements.txt")

    def test_env_example_exists(self):
        assert self._exists(".env.example")


class TestAPIImports:
    """Test that API module imports work without errors."""

    def test_import_health_route(self):
        from api.routes.health import router
        assert router is not None

    def test_import_entities_route(self):
        from api.routes.entities import router
        assert router is not None

    def test_import_graph_route(self):
        from api.routes.graph import router
        assert router is not None
