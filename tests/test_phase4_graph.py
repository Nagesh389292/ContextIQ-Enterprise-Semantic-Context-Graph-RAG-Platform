"""
Phase 4 tests — Neo4j Knowledge Graph, Semantic Mapping Layer, and API routes.
"""

import pytest
from pathlib import Path
from semantic.mapper import ConceptMapper
from semantic.entity_resolver import EntityResolver
from graph.schema import NODE_LABELS, RELATIONSHIP_TYPES
from graph.service import GraphService, get_graph_service
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)
ROOT = Path(__file__).parent.parent


class TestSemanticMappingLayer:

    def test_concept_mapper_load(self):
        mapper = ConceptMapper()
        assert "Machine" in mapper.configs
        assert "Supplier" in mapper.configs

    def test_harmonize_raw_headers(self):
        mapper = ConceptMapper()
        raw = {"equipment_code": "M001", "equipment_name": "CNC Lathe", "facility_code": "P001"}
        harmonized = mapper.harmonize_record(raw, "Machine")
        assert harmonized["machineId"] == "M001"
        assert harmonized["name"] == "CNC Lathe"
        assert harmonized["plantId"] == "P001"
        assert harmonized["_canonical_class"] == "Machine"

    def test_entity_resolver(self):
        resolver = EntityResolver()
        id_m, type_m, uri_m = resolver.resolve("M001")
        assert id_m == "M001"
        assert type_m == "Machine"
        assert "Machine" in uri_m

        id_p, type_p, _ = resolver.resolve("p001")
        assert id_p == "P001"
        assert type_p == "Plant"


class TestGraphSchemaAndService:

    def test_owl_mapping_alignment(self):
        assert NODE_LABELS["Machine"] == "Machine"
        assert RELATIONSHIP_TYPES["installedAt"] == "INSTALLED_AT"
        assert RELATIONSHIP_TYPES["hasSensor"] == "HAS_SENSOR"

    def test_graph_service_fallback(self):
        service = GraphService()
        stats = service.get_stats()
        assert "nodes" in stats
        assert "relationships" in stats

        nb = service.get_neighborhood("M001")
        assert "nodes" in nb
        assert "edges" in nb
        assert len(nb["nodes"]) >= 3


class TestGraphAPIRoutes:

    def test_get_graph_stats(self):
        res = client.get("/api/v1/graph/stats")
        assert res.status_code == 200
        data = res.json()
        assert "nodes" in data
        assert "relationships" in data

    def test_get_graph_entity(self):
        res = client.get("/api/v1/graph/entities/M001")
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == "M001"
        assert data["type"] == "Machine"

    def test_get_graph_neighborhood(self):
        res = client.get("/api/v1/graph/neighborhood/M001")
        assert res.status_code == 200
        data = res.json()
        assert "nodes" in data
        assert "edges" in data

    def test_search_graph_nodes(self):
        res = client.get("/api/v1/graph/search?q=M001")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert data[0]["id"] == "M001"

    def test_get_graph_relationships(self):
        res = client.get("/api/v1/graph/relationships/M001")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert len(data) >= 2
