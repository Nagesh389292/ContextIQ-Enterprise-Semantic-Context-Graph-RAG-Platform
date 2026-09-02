"""
ContextIQ — Document-to-Knowledge Graph Linker
Extracts enterprise domain entities from document text and creates Cypher (:Document)-[:MENTIONS]->(:Entity) relationships in Neo4j.
"""

import re
from typing import Dict, Any, List, Set
from loguru import logger
from semantic.entity_resolver import EntityResolver
from graph.service import get_graph_service

resolver = EntityResolver()


class GraphLinker:
    """Extracts enterprise entities from documents and links them to Neo4j knowledge graph nodes."""

    def extract_entities(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract canonical entities (Machines, Plants, Sensors, Suppliers, Materials, Orders)."""
        entities: Set[str] = set()

        # Regex patterns for domain entity codes
        machine_matches = re.findall(r"\bM\d{3}\b", text)
        plant_matches = re.findall(r"\bP\d{3}\b", text)
        supplier_matches = re.findall(r"\bS\d{3}\b", text)
        sensor_matches = re.findall(r"\bSN\d{3}\b", text)
        po_matches = re.findall(r"\bPO-\d{5}\b", text)
        mat_matches = re.findall(r"\bMAT-\d{3}\b", text)
        gb_matches = re.findall(r"\bGB-\d{3}\b", text)
        rc_matches = re.findall(r"\bRC-\d{2}\b", text)
        cmm_matches = re.findall(r"\bCMM-\d{2}\b", text)
        doc_matches = re.findall(r"\bDOC-\d{3}\b", text)
        qe_matches = re.findall(r"\bQE-\d{5}\b", text)

        for match in machine_matches + plant_matches + supplier_matches + sensor_matches + po_matches + mat_matches + gb_matches + rc_matches + cmm_matches + doc_matches + qe_matches:
            entities.add(match)

        # Include explicit metadata entity references if present
        for key in ["machine_id", "plant_id", "supplier_id"]:
            if metadata.get(key):
                entities.add(metadata[key])

        results = []
        for raw_id in entities:
            canonical_id, entity_type, ontology_uri = resolver.resolve(raw_id)
            results.append({
                "raw_id": raw_id,
                "canonical_id": canonical_id,
                "entity_type": entity_type,
                "ontology_uri": ontology_uri,
            })
        return results

    def link_document_to_graph(self, doc_metadata: Dict[str, Any], text: str) -> bool:
        """Create (:Document) node and MERGE relationships to entity nodes in Neo4j."""
        graph_service = get_graph_service()
        if not graph_service.is_healthy() or not graph_service.driver:
            logger.warning("Skipping Neo4j document graph linking: Driver offline.")
            return False

        doc_id = doc_metadata.get("document_id")
        doc_title = doc_metadata.get("title", "Document")
        doc_type = doc_metadata.get("document_type", "Manual")

        extracted_entities = self.extract_entities(text, doc_metadata)

        try:
            with graph_service.driver.session() as session:
                # 1. MERGE Document node
                session.run(
                    """
                    MERGE (d:Document {document_id: $doc_id})
                    SET d.title = $title, d.document_type = $doc_type
                    """,
                    doc_id=doc_id, title=doc_title, doc_type=doc_type
                )

                # 2. MERGE Relationships to extracted entities
                for ent in extracted_entities:
                    cid = ent["canonical_id"]
                    etype = ent["entity_type"]

                    if etype == "Machine":
                        session.run(
                            """
                            MATCH (d:Document {document_id: $doc_id})
                            MERGE (m:Machine {machine_id: $cid})
                            MERGE (d)-[:MENTIONS]->(m)
                            """,
                            doc_id=doc_id, cid=cid
                        )
                    elif etype == "Plant":
                        session.run(
                            """
                            MATCH (d:Document {document_id: $doc_id})
                            MERGE (p:Plant {plant_id: $cid})
                            MERGE (d)-[:APPLIES_TO]->(p)
                            """,
                            doc_id=doc_id, cid=cid
                        )
                    elif etype == "Supplier":
                        session.run(
                            """
                            MATCH (d:Document {document_id: $doc_id})
                            MERGE (s:Supplier {supplier_id: $cid})
                            MERGE (d)-[:MENTIONS]->(s)
                            """,
                            doc_id=doc_id, cid=cid
                        )
                    elif etype == "Sensor":
                        session.run(
                            """
                            MATCH (d:Document {document_id: $doc_id})
                            MERGE (sn:Sensor {sensor_id: $cid})
                            MERGE (d)-[:MENTIONS]->(sn)
                            """,
                            doc_id=doc_id, cid=cid
                        )
                    elif etype == "ProductionOrder":
                        session.run(
                            """
                            MATCH (d:Document {document_id: $doc_id})
                            MERGE (po:ProductionOrder {order_id: $cid})
                            MERGE (d)-[:RELEASES_ORDER]->(po)
                            """,
                            doc_id=doc_id, cid=cid
                        )
                    elif etype == "Material":
                        session.run(
                            """
                            MATCH (d:Document {document_id: $doc_id})
                            MERGE (mat:Material {material_id: $cid})
                            MERGE (d)-[:MENTIONS]->(mat)
                            """,
                            doc_id=doc_id, cid=cid
                        )

            return True
        except Exception as exc:
            logger.error(f"Error linking document {doc_id} to Neo4j: {exc}")
            return False
