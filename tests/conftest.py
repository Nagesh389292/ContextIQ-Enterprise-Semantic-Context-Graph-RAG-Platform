"""
Pytest configuration and shared fixtures.
"""

import pytest
from unittest.mock import MagicMock


# ── Settings override for tests ──────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def test_settings(tmp_path_factory):
    """Override settings for test environment."""
    import os
    os.environ.setdefault("APP_ENV", "test")
    os.environ.setdefault("POSTGRES_HOST", "localhost")
    os.environ.setdefault("GEMINI_API_KEY", "test_key_stub")


# ── Mock Neo4j driver ────────────────────────────────────────
@pytest.fixture
def mock_neo4j_driver():
    driver = MagicMock()
    session = MagicMock()
    driver.session.return_value.__enter__ = MagicMock(return_value=session)
    driver.session.return_value.__exit__ = MagicMock(return_value=False)
    return driver, session


# ── Mock ChromaDB client ─────────────────────────────────────
@pytest.fixture
def mock_chroma_client():
    client = MagicMock()
    collection = MagicMock()
    client.get_or_create_collection.return_value = collection
    collection.query.return_value = {
        "ids": [["chunk_001", "chunk_002"]],
        "documents": [["Temperature exceeds threshold.", "Check lubrication."]],
        "metadatas": [[
            {"document": "cnc_manual.txt", "section": "Bearing Maintenance"},
            {"document": "maintenance_sop.txt", "section": "Lubrication"},
        ]],
        "distances": [[0.12, 0.21]],
    }
    return client, collection


# ── Sample enterprise data ───────────────────────────────────
@pytest.fixture
def sample_machine():
    return {
        "machine_id": "M001",
        "machine_type": "CNC",
        "plant_id": "P001",
        "line_id": "L001",
        "supplier_id": "S001",
        "manufacturer": "FANUC",
        "status": "operational",
        "installation_date": "2020-03-15",
    }


@pytest.fixture
def sample_maintenance_event():
    return {
        "event_id": "ME001",
        "machine_id": "M001",
        "event_type": "corrective",
        "description": "Bearing overheating — lubrication replenished",
        "timestamp": "2024-01-15T10:30:00",
        "technician_id": "E042",
        "duration_hours": 2.5,
    }
