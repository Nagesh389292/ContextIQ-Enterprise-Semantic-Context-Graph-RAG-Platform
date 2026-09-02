"""
ContextIQ — Vector Retriever
Wraps ChromaDB vector store similarity search.
"""

from typing import Dict, Any, List, Optional
from documents.indexing.vector_store import get_vector_store


class VectorRetriever:
    """Retriever for ChromaDB vector similarity search."""

    def __init__(self):
        self.vector_store = get_vector_store()

    def search(
        self,
        query: str,
        top_k: int = 10,
        where_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute vector search against ChromaDB."""
        results = self.vector_store.search(query=query, top_k=top_k, where_filter=where_filter)
        for r in results:
            r["retrieval_source"] = "vector_similarity"
        return results
