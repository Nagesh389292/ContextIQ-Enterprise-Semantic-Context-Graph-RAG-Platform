"""
ContextIQ — VectorStore Service (ChromaDB Integration)
Manages persistent ChromaDB vector storage, chunk indexing, metadata filtering, and similarity search.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from loguru import logger

from config import settings
from documents.embeddings.embedder import Embedder

_vector_store_instance: Optional["VectorStore"] = None


class VectorStore:
    """Persistent ChromaDB vector database service."""

    def __init__(self, persist_dir: str | None = None, collection_name: str | None = None):
        self.persist_dir = Path(persist_dir or settings.chroma_persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name or settings.chroma_collection_name
        self.embedder = Embedder()

        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """Upsert semantic chunks into ChromaDB with metadata and pre-generated embeddings."""
        if not chunks:
            return 0

        chunk_ids = [c["chunk_id"] for c in chunks]
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]

        # Generate vector embeddings
        embeddings = self.embedder.encode_batch(texts)

        self.collection.upsert(
            ids=chunk_ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )
        logger.info(f"Indexed {len(chunks)} chunks into ChromaDB collection '{self.collection_name}'.")
        return len(chunks)

    def search(
        self,
        query: str,
        top_k: int = 5,
        where_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        formatted_where = None
        if where_filter:
            if len(where_filter) == 1:
                formatted_where = where_filter
            elif len(where_filter) > 1:
                formatted_where = {"$and": [{k: v} for k, v in where_filter.items()]}

        query_embedding = self.embedder.encode_text(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=formatted_where,
            include=["documents", "metadatas", "distances"]
        )

        output = []
        if results and results["ids"] and results["ids"][0]:
            ids = results["ids"][0]
            docs = results["documents"][0] if results["documents"] else []
            metas = results["metadatas"][0] if results["metadatas"] else []
            dists = results["distances"][0] if results["distances"] else []

            for i in range(len(ids)):
                distance = dists[i] if i < len(dists) else 0.0
                similarity = round(max(0.0, 1.0 - distance), 4)

                output.append({
                    "chunk_id": ids[i],
                    "document_id": metas[i].get("document_id", "") if i < len(metas) else "",
                    "document_title": metas[i].get("document_title", "") if i < len(metas) else "",
                    "section": metas[i].get("section", "") if i < len(metas) else "",
                    "text": docs[i] if i < len(docs) else "",
                    "score": similarity,
                    "metadata": metas[i] if i < len(metas) else {},
                })

        return output

    def get_stats(self) -> Dict[str, Any]:
        """Return total indexed chunk count and ChromaDB health."""
        count = self.collection.count()
        return {
            "status": "healthy",
            "collection_name": self.collection_name,
            "total_chunks": count,
            "embedding_model": settings.embedding_model,
            "dimension": settings.embedding_dimension,
        }


def get_vector_store() -> VectorStore:
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance
