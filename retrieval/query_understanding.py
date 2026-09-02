"""
ContextIQ — Typed Query Understanding Layer
Analyzes user natural language queries into typed domain intents, extracted entities, and search parameters.
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from documents.entity_linking.graph_linker import GraphLinker


@dataclass
class QueryAnalysis:
    """Structured query analysis output."""
    raw_query: str
    intent: str  # maintenance, supplier, production, quality, graph_relationship, document_lookup, semantic, unsupported
    entities: List[str] = field(default_factory=list)
    entity_types: Dict[str, str] = field(default_factory=dict)
    keywords: List[str] = field(default_factory=list)
    domain_terms: List[str] = field(default_factory=list)
    confidence: float = 0.0
    suggested_filters: Dict[str, Any] = field(default_factory=dict)


class QueryUnderstandingEngine:
    """Typed query intent and entity classifier."""

    def __init__(self):
        self.linker = GraphLinker()

    def analyze(self, query: str) -> QueryAnalysis:
        """Analyze query text into structured intent, entity mapping, and search hints."""
        query_lower = query.lower()
        
        # 1. Extract canonical entities
        extracted = self.linker.extract_entities(query, metadata={})
        entities = [e["canonical_id"] for e in extracted]
        entity_types = {e["canonical_id"]: e["entity_type"] for e in extracted}
        
        # 2. Intent Detection via Domain Triggers & Keywords
        intent = "semantic"
        confidence = 0.5
        domain_terms = []

        maintenance_triggers = ["maintenance", "lubrication", "oil", "bearing", "spindle", "hydraulic", "vibration", "calibration", "coolant", "gearbox", "shutdown", "repair"]
        supplier_triggers = ["supplier", "vendor", "sla", "lead time", "delivery", "procurement", "spare parts", "penalty", "dual-sourcing", "material staging", "sourcing"]
        production_triggers = ["production", "robot", "welding", "rc-01", "cell", "tool wear", "offset", "milling", "setup", "oee", "assembly", "schedule", "operation manual"]
        quality_triggers = ["quality", "inspection", "cpk", "spc", "surface roughness", "quarantine", "non-conforming", "cmm", "tolerance", "audit", "defect"]
        unsupported_triggers = ["vacation", "marketing", "bonus", "salary", "sales manager", "quantum computing", "datacenter", "hr policy"]

        if any(w in query_lower for w in unsupported_triggers):
            intent = "unsupported"
            confidence = 0.95
        elif any(w in query_lower for w in maintenance_triggers):
            intent = "maintenance"
            confidence = 0.85
            domain_terms = [w for w in maintenance_triggers if w in query_lower]
        elif any(w in query_lower for w in supplier_triggers):
            intent = "supplier"
            confidence = 0.85
            domain_terms = [w for w in supplier_triggers if w in query_lower]
        elif any(w in query_lower for w in production_triggers):
            intent = "production"
            confidence = 0.85
            domain_terms = [w for w in production_triggers if w in query_lower]
        elif any(w in query_lower for w in quality_triggers):
            intent = "quality"
            confidence = 0.85
            domain_terms = [w for w in quality_triggers if w in query_lower]

        # 3. Extract keywords
        stopwords = {"what", "which", "where", "when", "how", "does", "apply", "applies", "the", "is", "for", "on", "at", "to", "in", "with", "and", "or", "a", "an", "should", "check", "required", "about", "are", "be"}
        words = re.findall(r"\b\w+\b", query_lower)
        keywords = [w for w in words if w not in stopwords and len(w) > 2]

        # 4. Determine high-confidence metadata filters (only if entity extraction is unambiguous)
        filters = {}
        if confidence >= 0.8:
            for eid, etype in entity_types.items():
                if etype == "Machine":
                    filters["machine_id"] = eid
                elif etype == "Plant":
                    filters["plant_id"] = eid
                elif etype == "Supplier":
                    filters["supplier_id"] = eid

        return QueryAnalysis(
            raw_query=query,
            intent=intent,
            entities=entities,
            entity_types=entity_types,
            keywords=keywords,
            domain_terms=domain_terms,
            confidence=confidence,
            suggested_filters=filters
        )


_query_engine_instance: Optional[QueryUnderstandingEngine] = None

def get_query_engine() -> QueryUnderstandingEngine:
    global _query_engine_instance
    if _query_engine_instance is None:
        _query_engine_instance = QueryUnderstandingEngine()
    return _query_engine_instance
