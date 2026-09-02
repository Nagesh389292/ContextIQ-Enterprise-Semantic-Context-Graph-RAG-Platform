"""
ContextIQ — OWL Ontology & SHACL Validation Engine
Uses rdflib and pyshacl for RDF triple loading, SPARQL querying, and SHACL constraint checks.
"""

from pathlib import Path
from typing import Dict, List, Any
import rdflib
from rdflib import Graph, Namespace, RDF, RDFS, OWL
from pyshacl import validate
from loguru import logger

from config import settings

NS = Namespace(settings.ontology_namespace)


class OntologyValidator:
    """Validator and query engine for RDF/OWL ontology and SHACL shapes."""

    def __init__(self, ontology_path: Path | None = None, shapes_path: Path | None = None):
        self.ontology_path = ontology_path or settings.ontology_path / "enterprise.ttl"
        self.shapes_path = shapes_path or settings.ontology_path / "shapes.ttl"
        self.graph = Graph()
        self.shapes_graph = Graph()
        self.load_ontology()

    def load_ontology(self) -> None:
        """Load enterprise.ttl and shapes.ttl into RDFLib Graphs."""
        if self.ontology_path.exists():
            self.graph.parse(str(self.ontology_path), format="turtle")
            logger.info(f"Loaded ontology graph: {len(self.graph)} triples")
        else:
            logger.warning(f"Ontology file not found: {self.ontology_path}")

        if self.shapes_path.exists():
            self.shapes_graph.parse(str(self.shapes_path), format="turtle")
            logger.info(f"Loaded SHACL shapes graph: {len(self.shapes_graph)} triples")

    def get_classes(self) -> List[Dict[str, Any]]:
        """Return list of all OWL classes in the ontology."""
        sparql_path = settings.ontology_path / "sparql" / "list_classes.rq"
        if sparql_path.exists():
            query_str = sparql_path.read_text(encoding="utf-8")
            results = self.graph.query(query_str)
            classes = []
            for row in results:
                classes.append({
                    "class": str(row.get("class")),
                    "name": str(row.get("class")).split("#")[-1],
                    "label": str(row.get("label")) if row.get("label") else str(row.get("class")).split("#")[-1],
                    "comment": str(row.get("comment")) if row.get("comment") else "",
                    "superClass": str(row.get("superClass")).split("#")[-1] if row.get("superClass") else None,
                })
            return classes

        # Fallback using direct RDFLib triple matching
        classes = []
        for s in self.graph.subjects(RDF.type, OWL.Class):
            name = str(s).split("#")[-1]
            label = self.graph.value(s, RDFS.label)
            comment = self.graph.value(s, RDFS.comment)
            classes.append({
                "class": str(s),
                "name": name,
                "label": str(label) if label else name,
                "comment": str(comment) if comment else "",
                "superClass": None,
            })
        return classes

    def validate_data(self, data_graph: Graph) -> Dict[str, Any]:
        """Validate a data graph against enterprise SHACL shapes."""
        conforms, report_graph, report_text = validate(
            data_graph=data_graph,
            shacl_graph=self.shapes_graph,
            ont_graph=self.graph,
            inference="rdfs",
            abort_on_first=False,
            meta_shacl=False,
            debug=False,
        )

        results = []
        for s, p, o in report_graph:
            if (s, RDF.type, rdflib.URIRef("http://www.w3.org/ns/shacl#ValidationResult")) in report_graph:
                message = report_graph.value(s, rdflib.URIRef("http://www.w3.org/ns/shacl#resultMessage"))
                focus = report_graph.value(s, rdflib.URIRef("http://www.w3.org/ns/shacl#focusNode"))
                severity = report_graph.value(s, rdflib.URIRef("http://www.w3.org/ns/shacl#resultSeverity"))
                if message:
                    results.append({
                        "focus_node": str(focus).split("#")[-1] if focus else "Unknown",
                        "message": str(message),
                        "severity": str(severity).split("#")[-1] if severity else "Violation",
                    })

        return {
            "conforms": conforms,
            "validation_rate": 100.0 if conforms else round(max(0.0, 100.0 - (len(results) * 2.5)), 1),
            "issue_count": len(results),
            "issues": results,
            "report_text": report_text,
        }
