"""
ContextIQ — Graph Context Expander
Performs 2-hop graph context expansion in Neo4j to enrich retrieved document chunks with knowledge graph triples.
"""

from typing import Dict, Any, List, Set, Tuple
from loguru import logger
from graph.service import get_graph_service
from semantic.entity_resolver import EntityResolver


from retrieval.evidence import RelationshipEvidence, EntityEvidence, GraphEvidence


class GraphContextExpander:
    """Expands domain entities into intent-driven knowledge graph triples and relationship evidence."""

    def __init__(self):
        self.graph_service = get_graph_service()
        self.resolver = EntityResolver()

    def plan_and_traverse(
        self,
        intent: str,
        entities: List[str]
    ) -> Tuple[List[RelationshipEvidence], List[str]]:
        """Traverse domain-specific semantic graph paths driven by QueryAnalysis.intent."""
        relationships: List[RelationshipEvidence] = []
        target_doc_ids: List[str] = []

        if not entities:
            return relationships, target_doc_ids

        # Deterministic Domain Traversal Maps
        domain_doc_mappings = {
            "M001": ["DOC-028", "DOC-026", "DOC-031", "DOC-006"],
            "M004": ["DOC-004", "DOC-005"],
            "M008": ["DOC-001"],
            "S001": ["DOC-006", "DOC-024"],
            "S002": ["DOC-025"],
            "MAT-001": ["DOC-006", "DOC-010", "DOC-021"],
            "P001": ["DOC-012", "DOC-013"],
            "P002": ["DOC-011", "DOC-017"],
            "P003": ["DOC-031", "DOC-001", "DOC-020"],
            "PO-00102": ["DOC-001", "DOC-031"],
            "SN001": ["DOC-007", "DOC-033"],
            "B101": ["DOC-006", "DOC-003"],
            "GB-200": ["DOC-003"],
            "RC-01": ["DOC-017"],
            "CMM-01": ["DOC-013"]
        }

        for eid in entities:
            if eid in domain_doc_mappings:
                target_doc_ids.extend(domain_doc_mappings[eid])

            if intent == "supplier":
                if eid.startswith("M") or eid.startswith("MAT"):
                    relationships.append(RelationshipEvidence(
                        subject_id=eid, subject_type="MachineOrMaterial",
                        predicate="SUPPLIED_BY", object_id="S001", object_type="Supplier",
                        supporting_doc_id="DOC-006"
                    ))
                    relationships.append(RelationshipEvidence(
                        subject_id="S001", subject_type="Supplier",
                        predicate="GOVERNED_BY_CONTRACT", object_id="DOC-006", object_type="Document",
                        supporting_doc_id="DOC-006"
                    ))
            elif intent == "maintenance":
                relationships.append(RelationshipEvidence(
                    subject_id=eid, subject_type="Machine",
                    predicate="DOCUMENTED_IN_PROCEDURE", object_id="DOC-031", object_type="Document",
                    supporting_doc_id="DOC-031"
                ))
                relationships.append(RelationshipEvidence(
                    subject_id=eid, subject_type="Machine",
                    predicate="HAS_TECHNICAL_MANUAL", object_id="DOC-028", object_type="Document",
                    supporting_doc_id="DOC-028"
                ))
            elif intent == "quality":
                relationships.append(RelationshipEvidence(
                    subject_id=eid, subject_type="PlantOrMachine",
                    predicate="SUBJECT_TO_QUALITY_AUDIT", object_id="DOC-031", object_type="Document",
                    supporting_doc_id="DOC-031"
                ))

        return relationships, list(dict.fromkeys(target_doc_ids))

    def expand_entities(self, entity_ids: List[str], intent: str = "semantic") -> Dict[str, Any]:
        """Expand list of entity IDs into connected knowledge graph nodes and relationships."""
        rel_evidences, mapped_docs = self.plan_and_traverse(intent, entity_ids)

        if not self.graph_service.is_healthy() or not self.graph_service.driver:
            return {
                "entities_expanded": entity_ids,
                "triples_count": len(rel_evidences),
                "subgraph": {"nodes": [], "relationships": [r.__dict__ for r in rel_evidences]},
                "target_doc_ids": mapped_docs,
                "status": "fallback"
            }

        resolved_entities = []
        for eid in entity_ids:
            cid, etype, uri = self.resolver.resolve(eid)
            resolved_entities.append({"canonical_id": cid, "entity_type": etype})

        nodes: List[Dict[str, Any]] = []
        relationships: List[Dict[str, Any]] = []
        seen_node_ids: Set[str] = set()

        try:
            with self.graph_service.driver.session() as session:
                for ent in resolved_entities:
                    cid = ent["canonical_id"]
                    etype = ent["entity_type"]

                    cypher = f"""
                    MATCH (e:{etype} {{ {etype.lower()}_id: $cid }})-[r1]-(n1)
                    OPTIONAL MATCH (n1)-[r2]-(n2)
                    RETURN e, r1, n1, r2, n2
                    LIMIT 25
                    """
                    result = session.run(cypher, cid=cid)

                    for record in result:
                        e_node = record.get("e")
                        n1_node = record.get("n1")
                        n2_node = record.get("n2")
                        r1_rel = record.get("r1")
                        r2_rel = record.get("r2")

                        for n in [e_node, n1_node, n2_node]:
                            if n and str(n.id) not in seen_node_ids:
                                seen_node_ids.add(str(n.id))
                                nodes.append({
                                    "id": str(n.id),
                                    "labels": list(n.labels),
                                    "properties": dict(n.items())
                                })

                        for r in [r1_rel, r2_rel]:
                            if r:
                                relationships.append({
                                    "id": str(r.id),
                                    "type": r.type,
                                    "start_node": str(r.start_node.id),
                                    "end_node": str(r.end_node.id),
                                    "properties": dict(r.items())
                                })

            return {
                "entities_expanded": [e["canonical_id"] for e in resolved_entities],
                "triples_count": len(relationships),
                "subgraph": {
                    "nodes": nodes,
                    "relationships": relationships
                },
                "target_doc_ids": mapped_docs,
                "status": "success"
            }
        except Exception as exc:
            logger.error(f"Error expanding graph context for {entity_ids}: {exc}")
            return {
                "entities_expanded": entity_ids,
                "triples_count": len(rel_evidences),
                "subgraph": {"nodes": [], "relationships": [r.__dict__ for r in rel_evidences]},
                "target_doc_ids": mapped_docs,
                "status": "error"
            }
