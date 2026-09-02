"""
ContextIQ — Knowledge Graph Service Layer
Provides Cypher query execution for neighborhood traversal, entity lookup, and graph statistics.
"""

from typing import Dict, List, Any, Optional
from neo4j import GraphDatabase, Driver
from loguru import logger
from config import settings

_graph_service_instance: Optional["GraphService"] = None


class GraphService:
    """Service wrapping Neo4j Cypher queries with graceful fallback if Neo4j is offline."""

    def __init__(self, uri: str | None = None, user: str | None = None, password: str | None = None):
        self.uri = uri or settings.neo4j_uri
        self.user = user or settings.neo4j_user
        self.password = password or settings.neo4j_password
        self.driver: Driver | None = None
        self._is_connected = False
        self._try_connect()

    def _try_connect(self) -> bool:
        if getattr(self, "_failed_once", False):
            return False
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            self.driver.verify_connectivity()
            self._is_connected = True
            return True
        except Exception:
            self.driver = None
            self._is_connected = False
            self._failed_once = True
            return False

    def is_healthy(self) -> bool:
        """Returns True if connected to Neo4j."""
        if not self._is_connected or not self.driver:
            return self._try_connect()
        try:
            self.driver.verify_connectivity()
            return True
        except Exception:
            self._is_connected = False
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Return total node and relationship counts."""
        if not self.is_healthy() or not self.driver:
            return {
                "status": "offline",
                "nodes": 12450,
                "relationships": 31820,
                "is_demo": True,
            }

        try:
            with self.driver.session() as session:
                n_res = session.run("MATCH (n) RETURN count(n) AS c").single()
                r_res = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()
                return {
                    "status": "healthy",
                    "nodes": n_res["c"] if n_res else 0,
                    "relationships": r_res["c"] if r_res else 0,
                    "is_demo": False,
                }
        except Exception as exc:
            logger.error(f"Error fetching Neo4j stats: {exc}")
            return {"status": "error", "nodes": 0, "relationships": 0, "is_demo": True}

    def get_neighborhood(self, entity_id: str) -> Dict[str, Any]:
        """Return 1-hop / 2-hop graph neighborhood for React Flow canvas."""
        if not self.is_healthy() or not self.driver:
            # Explicit DEMO mode fallback
            return {
                "nodes": [
                    {"id": entity_id, "label": f"Machine {entity_id}", "type": "Machine", "properties": {"status": "operational"}},
                    {"id": "P001", "label": "Northgate Plant (P001)", "type": "Plant", "properties": {"location": "Detroit, MI"}},
                    {"id": "L001", "label": "Assembly Line A (L001)", "type": "ProductionLine", "properties": {"status": "active"}},
                    {"id": "SN001", "label": "Temp Sensor SN001", "type": "Sensor", "properties": {"unit": "°C"}},
                    {"id": "S001", "label": "Precision Bearings Inc (S001)", "type": "Supplier", "properties": {"tier": 1}},
                ],
                "edges": [
                    {"id": "e1", "source": entity_id, "target": "P001", "label": "INSTALLED_AT"},
                    {"id": "e2", "source": entity_id, "target": "L001", "label": "ON_LINE"},
                    {"id": "e3", "source": "SN001", "target": entity_id, "label": "ATTACHED_TO"},
                    {"id": "e4", "source": entity_id, "target": "S001", "label": "SUPPLIED_BY"},
                ],
                "is_demo": True,
            }

        try:
            nodes_dict = {}
            edges_list = []

            cypher = """
            MATCH (n {machine_id: $entity_id})
            OPTIONAL MATCH (n)-[r]-(m)
            RETURN n, r, m
            LIMIT 50
            """
            with self.driver.session() as session:
                results = session.run(cypher, entity_id=entity_id)
                for record in results:
                    n = record["n"]
                    m = record["m"]
                    r = record["r"]

                    if n:
                        nodes_dict[n.element_id] = {
                            "id": n.get("machine_id", entity_id),
                            "label": n.get("name", entity_id),
                            "type": list(n.labels)[0] if n.labels else "Entity",
                            "properties": dict(n),
                        }
                    if m:
                        nodes_dict[m.element_id] = {
                            "id": m.get("machine_id", m.get("plant_id", m.get("sensor_id", m.get("supplier_id", m.element_id)))),
                            "label": m.get("name", str(m.element_id)),
                            "type": list(m.labels)[0] if m.labels else "Entity",
                            "properties": dict(m),
                        }
                    if r:
                        edges_list.append({
                            "id": r.element_id,
                            "source": nodes_dict.get(r.start_node.element_id, {}).get("id", str(r.start_node.element_id)),
                            "target": nodes_dict.get(r.end_node.element_id, {}).get("id", str(r.end_node.element_id)),
                            "label": r.type,
                        })

            return {
                "nodes": list(nodes_dict.values()),
                "edges": edges_list,
                "is_demo": False,
            }
        except Exception as exc:
            logger.error(f"Error fetching neighborhood for {entity_id}: {exc}")
            return {"nodes": [], "edges": [], "is_demo": True}


def get_graph_service() -> GraphService:
    global _graph_service_instance
    if _graph_service_instance is None:
        _graph_service_instance = GraphService()
    return _graph_service_instance
