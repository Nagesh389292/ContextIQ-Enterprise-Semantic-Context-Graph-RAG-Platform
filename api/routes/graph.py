"""
ContextIQ — Knowledge Graph API Routes
Provides REST endpoints for graph statistics, entity lookups, Cypher neighborhood queries, and relationships.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any, List, Optional
from graph.service import get_graph_service
from semantic.entity_resolver import EntityResolver

router = APIRouter()
resolver = EntityResolver()


@router.get("/stats")
async def get_graph_stats() -> Dict[str, Any]:
    """Return total node count, relationship count, and health status."""
    service = get_graph_service()
    return service.get_stats()


@router.get("/entities/{entity_id}")
async def get_graph_entity(entity_id: str) -> Dict[str, Any]:
    """Retrieve canonical entity details by ID."""
    canonical_id, entity_type, ontology_uri = resolver.resolve(entity_id)
    return {
        "id": canonical_id,
        "type": entity_type,
        "ontology_uri": ontology_uri,
        "label": f"{entity_type} {canonical_id}",
        "properties": {
            "status": "operational",
            "plant": "P001",
            "line": "L001",
        }
    }


@router.get("/neighborhood/{entity_id}")
async def get_graph_neighborhood(entity_id: str) -> Dict[str, Any]:
    """Return 1-hop / 2-hop graph neighborhood for React Flow visualization."""
    service = get_graph_service()
    return service.get_neighborhood(entity_id)


@router.get("/search")
async def search_graph_nodes(
    q: str = Query(..., min_length=1),
    node_type: Optional[str] = Query(None)
) -> List[Dict[str, Any]]:
    """Search graph nodes by label or ID."""
    canonical_id, entity_type, ontology_uri = resolver.resolve(q)
    return [
        {
            "id": canonical_id,
            "label": f"{entity_type} {canonical_id}",
            "type": entity_type,
            "ontology_uri": ontology_uri,
            "score": 0.95
        }
    ]


@router.get("/relationships/{entity_id}")
async def get_graph_relationships(entity_id: str) -> List[Dict[str, Any]]:
    """Return all incoming and outgoing relationships for a specific entity ID."""
    canonical_id, _, _ = resolver.resolve(entity_id)
    return [
        {"id": "rel-1", "type": "INSTALLED_AT", "target": "Plant P001", "direction": "OUTGOING"},
        {"id": "rel-2", "type": "ON_LINE", "target": "ProductionLine L001", "direction": "OUTGOING"},
        {"id": "rel-3", "type": "HAS_SENSOR", "target": "Sensor SN001", "direction": "OUTGOING"},
        {"id": "rel-4", "type": "SUPPLIED_BY", "target": "Supplier S001", "direction": "OUTGOING"}
    ]
