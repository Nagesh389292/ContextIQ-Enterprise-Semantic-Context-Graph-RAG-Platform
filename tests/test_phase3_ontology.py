"""
Phase 3 tests — Ontology & SHACL Validation Engine.
"""

from pathlib import Path
import pytest
from ontology.validator import OntologyValidator
from ontology.service import OntologyService

ROOT = Path(__file__).parent.parent


class TestOntologyEngine:

    def test_files_exist(self):
        assert (ROOT / "ontology" / "enterprise.ttl").exists()
        assert (ROOT / "ontology" / "shapes.ttl").exists()

    def test_ontology_validator_load(self):
        validator = OntologyValidator()
        assert len(validator.graph) > 0
        assert len(validator.shapes_graph) > 0

    def test_get_classes(self):
        validator = OntologyValidator()
        classes = validator.get_classes()
        assert len(classes) >= 10
        names = [c["name"] for c in classes]
        assert "Machine" in names
        assert "Plant" in names
        assert "Supplier" in names
        assert "Sensor" in names
        assert "ProductionOrder" in names

    def test_ontology_service(self):
        service = OntologyService()
        classes = service.list_classes()
        assert len(classes) >= 10

        machine_details = service.get_class_details("Machine")
        assert machine_details is not None
        assert "installedAt" in str(machine_details["object_properties"])
        assert "hasSensor" in str(machine_details["object_properties"])

    def test_shacl_validation_summary(self):
        service = OntologyService()
        summary = service.get_shacl_validation_summary()
        assert summary["validation_rate"] > 90.0
        assert len(summary["issues"]) > 0
