"""
ContextIQ — Document Intelligence Master Service
Coordinates document loading, semantic chunking, entity resolution, Neo4j graph linking, and ChromaDB indexing.
"""

from typing import Dict, Any, List, Optional
from loguru import logger

from documents.loaders.doc_loader import DocumentLoader
from documents.chunking.semantic_chunker import SemanticChunker
from documents.entity_linking.graph_linker import GraphLinker
from documents.indexing.vector_store import get_vector_store

_doc_service_instance: Optional["DocumentService"] = None


class DocumentService:
    """Master service for enterprise document intelligence."""

    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = SemanticChunker()
        self.linker = GraphLinker()
        self.vector_store = get_vector_store()

    def ingest_all_documents(self) -> Dict[str, Any]:
        """Ingest all synthetic enterprise documents, extract entities, link to Neo4j graph, and index in ChromaDB."""
        docs = self.loader.load_all()
        total_docs = len(docs)
        total_chunks = 0
        total_linked_docs = 0

        for metadata, body in docs:
            # 1. Semantic Chunking
            chunks = self.chunker.chunk_document(metadata, body)
            if chunks:
                self.vector_store.add_chunks(chunks)
                total_chunks += len(chunks)

            # 2. Graph Entity Linking in Neo4j
            linked = self.linker.link_document_to_graph(metadata, body)
            if linked:
                total_linked_docs += 1

        logger.info(f"Ingested {total_docs} documents ({total_chunks} chunks, {total_linked_docs} graph links).")
        return {
            "total_documents": total_docs,
            "total_chunks": total_chunks,
            "graph_linked_documents": total_linked_docs,
            "status": "completed",
        }

    def list_documents(self) -> List[Dict[str, Any]]:
        """List all enterprise documents with metadata."""
        docs = self.loader.load_all()
        result = []
        for metadata, body in docs:
            entities = self.linker.extract_entities(body, metadata)
            result.append({
                "document_id": metadata.get("document_id"),
                "title": metadata.get("title"),
                "document_type": metadata.get("document_type"),
                "process": metadata.get("process"),
                "plant_id": metadata.get("plant_id"),
                "machine_id": metadata.get("machine_id"),
                "supplier_id": metadata.get("supplier_id"),
                "effective_date": metadata.get("effective_date"),
                "entities_count": len(entities),
                "entities": entities,
                "status": "Indexed",
            })
        return result

    def get_document_details(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get full details, metadata, and extracted entities for a single document ID."""
        docs = self.list_documents()
        target = next((d for d in docs if d["document_id"].upper() == doc_id.upper()), None)
        if not target:
            return None

        # Load document body
        doc_file = self.loader.raw_dir / f"{target['document_id']}.md"
        metadata, body = self.loader.load_document(doc_file)
        chunks = self.chunker.chunk_document(metadata, body)

        return {
            **target,
            "body": body,
            "chunks_count": len(chunks),
            "chunks": chunks,
        }

    def search_vector_store(
        self,
        query: str,
        top_k: int = 5,
        plant_id: Optional[str] = None,
        doc_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Perform similarity search with metadata filter."""
        where_filter = {}
        if plant_id:
            where_filter["plant_id"] = plant_id
        if doc_type:
            where_filter["document_type"] = doc_type

        return self.vector_store.search(query, top_k=top_k, where_filter=where_filter if where_filter else None)


def get_document_service() -> DocumentService:
    global _doc_service_instance
    if _doc_service_instance is None:
        _doc_service_instance = DocumentService()
    return _doc_service_instance
