"""
ContextIQ — Typed Semantic Evidence Model
Defines structured evidence objects preserving domain relationships, entity provenance, and document sources for Graph-RAG.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class DocumentEvidence:
    """Document section chunk evidence."""
    chunk_id: str
    document_id: str
    document_title: str
    section: str
    text: str
    score: float
    matched_sources: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EntityEvidence:
    """Canonical domain entity evidence."""
    canonical_id: str
    entity_type: str
    raw_id: str
    ontology_uri: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RelationshipEvidence:
    """Knowledge graph semantic triple relationship evidence."""
    subject_id: str
    subject_type: str
    predicate: str
    object_id: str
    object_type: str
    supporting_doc_id: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEvidence:
    """Knowledge graph neighborhood subgraph evidence."""
    expanded_entities: List[str] = field(default_factory=list)
    triples_count: int = 0
    relationships: List[RelationshipEvidence] = field(default_factory=list)
    nodes: List[EntityEvidence] = field(default_factory=list)


@dataclass
class EvidenceBundle:
    """Master structured evidence container returned by retrieval engine."""
    query: str
    intent: str
    document_evidence: List[DocumentEvidence] = field(default_factory=list)
    entity_evidence: List[EntityEvidence] = field(default_factory=list)
    relationship_evidence: List[RelationshipEvidence] = field(default_factory=list)
    graph_evidence: Optional[GraphEvidence] = None
    total_retrieved: int = 0
    provenance: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize evidence bundle into structured API JSON format."""
        top_chunks = []
        for doc in self.document_evidence:
            top_chunks.append({
                "chunk_id": doc.chunk_id,
                "document_id": doc.document_id,
                "document_title": doc.document_title,
                "section": doc.section,
                "text": doc.text,
                "score": round(doc.score, 6),
                "rrf_score": round(doc.score, 6),
                "matched_sources": doc.matched_sources,
                "metadata": doc.metadata
            })

        rel_list = []
        for r in self.relationship_evidence:
            rel_list.append({
                "subject": f"{r.subject_type}:{r.subject_id}",
                "predicate": r.predicate,
                "object": f"{r.object_type}:{r.object_id}",
                "supporting_doc": r.supporting_doc_id
            })

        return {
            "query": self.query,
            "intent": self.intent,
            "total_retrieved_chunks": len(top_chunks),
            "top_chunks": top_chunks,
            "fused_results": top_chunks,
            "entities": [e.canonical_id for e in self.entity_evidence],
            "relationships": rel_list,
            "graph_context": {
                "entities_expanded": self.graph_evidence.expanded_entities if self.graph_evidence else [],
                "triples_count": self.graph_evidence.triples_count if self.graph_evidence else 0,
            },
            "provenance": self.provenance,
            "retrieval_metadata": {
                "query_intent": self.intent,
                "total_retrieved": self.total_retrieved
            }
        }
