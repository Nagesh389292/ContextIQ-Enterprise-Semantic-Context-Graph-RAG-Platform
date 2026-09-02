"""
ContextIQ — Neo4j Knowledge Graph Loader
Idempotent ETL script converting synthetic enterprise CSV records into Neo4j nodes and relationships.
"""

import csv
from pathlib import Path
from typing import Dict, Any, List
from neo4j import GraphDatabase, Driver
from loguru import logger

from config import settings
from semantic.mapper import ConceptMapper

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"


class Neo4jLoader:
    """Idempotent graph loader enforcing unique constraints and MERGE operations."""

    def __init__(self, uri: str | None = None, user: str | None = None, password: str | None = None):
        self.uri = uri or settings.neo4j_uri
        self.user = user or settings.neo4j_user
        self.password = password or settings.neo4j_password
        self.driver: Driver | None = None
        self.mapper = ConceptMapper()

    def connect(self) -> bool:
        """Establish Neo4j database driver session."""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            self.driver.verify_connectivity()
            logger.info("Connected to Neo4j database.")
            return True
        except Exception as exc:
            logger.error(f"Neo4j connection failed: {exc}")
            self.driver = None
            return False

    def close(self):
        if self.driver:
            self.driver.close()

    def init_schema(self):
        """Run constraints and index creation."""
        constraints_file = Path(__file__).parent / "queries" / "constraints.cypher"
        if not constraints_file.exists() or not self.driver:
            return

        cypher_statements = constraints_file.read_text(encoding="utf-8").split(";")
        with self.driver.session() as session:
            for stmt in cypher_statements:
                stmt = stmt.strip()
                if stmt and not stmt.startswith("//"):
                    try:
                        session.run(stmt)
                    except Exception as e:
                        logger.warning(f"Constraint creation notice: {e}")
        logger.info("Neo4j constraints & indexes initialized.")

    def seed_graph(self):
        """Load all CSV entities and relationships idempotently using MERGE."""
        if not self.driver:
            logger.warning("Skipping Neo4j seed: Driver disconnected.")
            return

        self.init_schema()

        # 1. Plants
        plants = self._load_csv("plants.csv")
        with self.driver.session() as session:
            for r in plants:
                session.run(
                    """
                    MERGE (p:Plant {plant_id: $plant_id})
                    SET p.name = $name, p.location = $location, p.country = $country
                    """,
                    plant_id=r["plant_id"], name=r["name"], location=r.get("location", ""), country=r.get("country", "")
                )

        # 2. Production Lines
        lines = self._load_csv("production_lines.csv")
        with self.driver.session() as session:
            for r in lines:
                session.run(
                    """
                    MERGE (l:ProductionLine {line_id: $line_id})
                    SET l.name = $name, l.line_type = $line_type, l.status = $status
                    WITH l
                    MATCH (p:Plant {plant_id: $plant_id})
                    MERGE (l)-[:LOCATED_AT]->(p)
                    """,
                    line_id=r["line_id"], name=r["name"], line_type=r.get("line_type", ""), status=r.get("status", "active"), plant_id=r.get("plant_id", "")
                )

        # 3. Suppliers
        suppliers = self._load_csv("suppliers.csv")
        with self.driver.session() as session:
            for r in suppliers:
                session.run(
                    """
                    MERGE (s:Supplier {supplier_id: $supplier_id})
                    SET s.name = $name, s.country = $country, s.rating = toFloat($rating), s.tier = toInteger($tier)
                    """,
                    supplier_id=r["supplier_id"], name=r["name"], country=r.get("country", ""), rating=r.get("rating", 4.5), tier=r.get("tier", 1)
                )

        # 4. Machines (OWL: Machine installedAt Plant, onLine Line, suppliedBy Supplier)
        machines = self._load_csv("machines.csv")
        with self.driver.session() as session:
            for r in machines:
                h = self.mapper.harmonize_record(r, "Machine")
                session.run(
                    """
                    MERGE (m:Machine {machine_id: $machine_id})
                    SET m.name = $name, m.machine_type = $machine_type, m.status = $status, m.manufacturer = $manufacturer
                    WITH m
                    MATCH (p:Plant {plant_id: $plant_id})
                    MERGE (m)-[:INSTALLED_AT]->(p)
                    WITH m
                    MATCH (l:ProductionLine {line_id: $line_id})
                    MERGE (m)-[:ON_LINE]->(l)
                    WITH m
                    MATCH (s:Supplier {supplier_id: $supplier_id})
                    MERGE (m)-[:SUPPLIED_BY]->(s)
                    """,
                    machine_id=h["machineId"], name=h.get("name", ""), machine_type=h.get("machineType", ""),
                    status=h.get("status", "operational"), manufacturer=h.get("manufacturer", ""),
                    plant_id=h.get("plantId", ""), line_id=h.get("lineId", ""), supplier_id=h.get("supplierId", "")
                )

        # 5. Sensors (OWL: Sensor attachedToMachine Machine)
        sensors = self._load_csv("sensors.csv")
        with self.driver.session() as session:
            for r in sensors:
                session.run(
                    """
                    MERGE (sn:Sensor {sensor_id: $sensor_id})
                    SET sn.sensor_type = $sensor_type, sn.unit = $unit, sn.status = $status
                    WITH sn
                    MATCH (m:Machine {machine_id: $machine_id})
                    MERGE (sn)-[:ATTACHED_TO]->(m)
                    MERGE (m)-[:HAS_SENSOR]->(sn)
                    """,
                    sensor_id=r["sensor_id"], sensor_type=r.get("sensor_type", ""), unit=r.get("unit", ""),
                    status=r.get("status", "active"), machine_id=r.get("machine_id", "")
                )

        logger.info("Idempotent Neo4j Knowledge Graph load complete.")

    def _load_csv(self, filename: str) -> List[Dict[str, Any]]:
        path = RAW_DIR / filename
        if not path.exists():
            return []
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
