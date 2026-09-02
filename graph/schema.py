"""
ContextIQ — Neo4j Knowledge Graph Schema & OWL Mapping
Defines canonical node labels, property keys, and relationship types mapped to OWL ontology.
"""

# OWL Classes → Neo4j Node Labels
NODE_LABELS = {
    "Plant": "Plant",
    "ProductionLine": "ProductionLine",
    "Machine": "Machine",
    "Sensor": "Sensor",
    "Supplier": "Supplier",
    "Material": "Material",
    "Employee": "Employee",
    "ProductionOrder": "ProductionOrder",
    "MaintenanceEvent": "MaintenanceEvent",
    "QualityEvent": "QualityEvent",
}

# OWL Object Properties → Neo4j Relationship Types
RELATIONSHIP_TYPES = {
    "locatedAt": "LOCATED_AT",
    "installedAt": "INSTALLED_AT",
    "onLine": "ON_LINE",
    "hasSensor": "HAS_SENSOR",
    "attachedToMachine": "ATTACHED_TO",
    "suppliedBy": "SUPPLIED_BY",
    "suppliesMaterial": "SUPPLIES",
    "assignedToPlant": "ASSIGNED_TO",
    "maintainsMachine": "MAINTAINS",
    "performedBy": "PERFORMED_BY",
    "inspectsOrder": "INSPECTS",
    "relatesToMachine": "RELATES_TO",
}
