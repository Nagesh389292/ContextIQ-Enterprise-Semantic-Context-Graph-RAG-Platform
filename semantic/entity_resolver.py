"""
ContextIQ — Enterprise Entity Resolver
Resolves entity aliases, codes, and IDs to canonical URI identifiers.
"""

from typing import Dict, Any, Optional, Tuple


class EntityResolver:
    """Resolves raw entity references (e.g. 'M001', 'Machine_001') into canonical IDs and concepts."""

    def resolve(self, raw_identifier: str, default_type: str = "Machine") -> Tuple[str, str, str]:
        """
        Returns (canonical_id, entity_type, ontology_uri)
        Example: 'M001' -> ('M001', 'Machine', 'http://enterprise-sce.org/ontology#Machine')
        """
        clean_id = raw_identifier.strip().upper()

        if clean_id.startswith("M") and len(clean_id) == 4 and clean_id[1:].isdigit():
            return (clean_id, "Machine", "http://enterprise-sce.org/ontology#Machine")

        if clean_id.startswith("P") and len(clean_id) == 4 and clean_id[1:].isdigit():
            return (clean_id, "Plant", "http://enterprise-sce.org/ontology#Plant")

        if clean_id.startswith("S") and len(clean_id) == 4 and clean_id[1:].isdigit():
            return (clean_id, "Supplier", "http://enterprise-sce.org/ontology#Supplier")

        if clean_id.startswith("SN") and len(clean_id) == 5 and clean_id[2:].isdigit():
            return (clean_id, "Sensor", "http://enterprise-sce.org/ontology#Sensor")

        if clean_id.startswith("PO-") or clean_id.startswith("PO"):
            formatted = clean_id if clean_id.startswith("PO-") else f"PO-{clean_id[2:]}"
            return (formatted, "ProductionOrder", "http://enterprise-sce.org/ontology#ProductionOrder")

        return (clean_id, default_type, f"http://enterprise-sce.org/ontology#{default_type}")
