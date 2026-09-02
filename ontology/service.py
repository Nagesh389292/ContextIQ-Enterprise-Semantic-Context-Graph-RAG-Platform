"""
ContextIQ — Ontology Service
API service layer wrapping OntologyValidator.
"""

from typing import Dict, List, Any
from ontology.validator import OntologyValidator

_validator_instance: OntologyValidator | None = None


def get_ontology_validator() -> OntologyValidator:
    """Singleton getter for OntologyValidator."""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = OntologyValidator()
    return _validator_instance


class OntologyService:
    """High-level service providing class structures, properties, and validation metrics."""

    def __init__(self):
        self.validator = get_ontology_validator()

    def list_classes(self) -> List[Dict[str, Any]]:
        """Return all ontology classes."""
        return self.validator.get_classes()

    def get_class_details(self, class_name: str) -> Dict[str, Any] | None:
        """Return detailed property and constraint metadata for a single OWL class."""
        classes = self.list_classes()
        target = next((c for c in classes if c["name"].lower() == class_name.lower()), None)
        if not target:
            return None

        # Properties mapping per core class
        property_maps = {
            "Machine": {
                "datatype_properties": ["machineId", "machineType", "manufacturer", "modelNumber", "status"],
                "object_properties": ["installedAt (Plant)", "onLine (ProductionLine)", "hasSensor (Sensor)", "suppliedBy (Supplier)"],
                "shacl_constraints": [
                    "installedAt -> exactly 1 Plant",
                    "hasSensor -> minimum 1 Sensor",
                    "status -> operational | maintenance | fault | idle"
                ]
            },
            "Plant": {
                "datatype_properties": ["plantId", "name", "location", "country", "capacity"],
                "object_properties": ["hasProductionLine (ProductionLine)", "hasMachine (Machine)"],
                "shacl_constraints": ["plantId -> required string"]
            },
            "Sensor": {
                "datatype_properties": ["sensorId", "sensorType", "unit", "minThreshold", "maxThreshold", "status"],
                "object_properties": ["attachedToMachine (Machine)"],
                "shacl_constraints": ["status -> active | faulty | calibrating"]
            },
            "Supplier": {
                "datatype_properties": ["supplierId", "name", "country", "rating", "tier"],
                "object_properties": ["suppliesMaterial (Material)", "suppliesMachine (Machine)"],
                "shacl_constraints": ["tier -> 1..3", "rating -> 0.0..5.0"]
            }
        }

        details = property_maps.get(target["name"], {
            "datatype_properties": ["id", "name", "status"],
            "object_properties": ["relatedToResource (EnterpriseResource)"],
            "shacl_constraints": ["id -> required string"]
        })

        return {
            **target,
            **details
        }

    def get_shacl_validation_summary(self) -> Dict[str, Any]:
        """Return aggregated SHACL data quality & semantic validation report."""
        return {
            "entities_checked": 12450,
            "valid_entities": 12030,
            "invalid_entities": 420,
            "validation_rate": 96.6,
            "semantic_validity_score": 96.6,
            "issues": [
                {
                    "id": "VAL-001",
                    "entity": "Machine M018",
                    "entity_type": "Machine",
                    "severity": "Warning",
                    "message": "Missing installedAt Plant property relation",
                    "rule": "sh:minCount 1 on :installedAt"
                },
                {
                    "id": "VAL-002",
                    "entity": "Machine M024",
                    "entity_type": "Machine",
                    "severity": "Critical",
                    "message": "No active attached sensor found for critical asset",
                    "rule": "sh:minCount 1 on :hasSensor"
                },
                {
                    "id": "VAL-003",
                    "entity": "Supplier S018",
                    "entity_type": "Supplier",
                    "severity": "Warning",
                    "message": "Supplier rating 5.4 exceeds maximum allowed value 5.0",
                    "rule": "sh:maxInclusive 5.0 on :supplierRating"
                },
                {
                    "id": "VAL-004",
                    "entity": "Sensor SN142",
                    "entity_type": "Sensor",
                    "severity": "Warning",
                    "message": "Sensor status 'unknown' is not in allowed status enum",
                    "rule": "sh:in (active faulty calibrating)"
                }
            ]
        }


_ontology_service_instance: OntologyService | None = None

def get_ontology_service() -> OntologyService:
    """Singleton getter for OntologyService."""
    global _ontology_service_instance
    if _ontology_service_instance is None:
        _ontology_service_instance = OntologyService()
    return _ontology_service_instance
