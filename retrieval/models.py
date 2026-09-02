"""
ContextIQ — Hybrid Retrieval Data Models
Provides structured, typed container for hybrid retrieval results and provenance.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    """Represents a single retrieved semantic chunk with full provenance."""
    chunk_id: str
    document_id: str
    document_title: str
    section: str
    text: str
    score: float
    rrf_score: Optional[float] = None
    rrf_rank: Optional[int] = None
    matched_sources: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    linked_entities: List[str] = Field(default_factory=list)


class GraphTriple(BaseModel):
    """Represents a single knowledge graph relationship triple."""
    start_node_id: str
    start_node_label: str
    relationship_type: str
    end_node_id: str
    end_node_label: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphSubContext(BaseModel):
    """Container for expanded 2-hop Neo4j subgraph context."""
    entities_expanded: List[str] = Field(default_factory=list)
    triples_count: int = 0
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    relationships: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "success"


class HybridRetrievalResult(BaseModel):
    """Master retrieval result bundle decoupled from LLM generation."""
    query: str
    lexical_results: List[RetrievedChunk] = Field(default_factory=list)
    vector_results: List[RetrievedChunk] = Field(default_factory=list)
    fused_results: List[RetrievedChunk] = Field(default_factory=list)
    graph_context: GraphSubContext = Field(default_factory=GraphSubContext)
    entities: List[str] = Field(default_factory=list)
    filters: Dict[str, Any] = Field(default_factory=dict)
    provenance: Dict[str, Any] = Field(default_factory=dict)
    retrieval_metadata: Dict[str, Any] = Field(default_factory=dict)
