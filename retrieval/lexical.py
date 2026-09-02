"""
ContextIQ — BM25 Lexical Keyword Retriever
Provides BM25 keyword search over document section chunks for exact serial numbers, error codes, and equipment tags.
"""

import re
from typing import Dict, Any, List, Optional
from rank_bm25 import BM25Okapi
from loguru import logger
from documents.service import get_document_service


class BM25LexicalRetriever:
    """BM25 keyword search index built over document corpus section chunks."""

    def __init__(self):
        self.doc_service = get_document_service()
        self._bm25: Optional[BM25Okapi] = None
        self._chunks: List[Dict[str, Any]] = []
        self._is_indexed = False

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into lowercase terms, preserving hyphenated entity codes and filtering stop words."""
        stopwords = {
            "what", "which", "where", "when", "how", "does", "apply", "applies", "the", "is",
            "for", "on", "at", "to", "in", "with", "and", "or", "a", "an", "should", "check",
            "required", "associated", "specified", "required", "relevant", "about", "are", "be",
            "this", "that", "from", "by", "as", "of"
        }
        # Extract hyphenated tokens (e.g. MAT-001, PO-00102, GB-200)
        raw_tokens = re.findall(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", text.lower())
        tokens = []
        for t in raw_tokens:
            if t in stopwords:
                continue
            tokens.append(t)
            # Also add unhyphenated form if hyphenated
            if "-" in t:
                tokens.append(t.replace("-", ""))
        return tokens

    def build_index(self, force: bool = False):
        """Build BM25 index over all document section chunks."""
        if self._is_indexed and not force:
            return

        docs = self.doc_service.list_documents()
        all_chunks = []
        tokenized_corpus = []

        for doc in docs:
            detail = self.doc_service.get_document_details(doc["document_id"])
            if detail and "chunks" in detail:
                for chunk in detail["chunks"]:
                    all_chunks.append(chunk)
                    tokens = self._tokenize(chunk["text"] + " " + chunk.get("section", ""))
                    tokenized_corpus.append(tokens)

        self._chunks = all_chunks
        if tokenized_corpus:
            self._bm25 = BM25Okapi(tokenized_corpus)
            self._is_indexed = True
            logger.info(f"Built BM25 index over {len(all_chunks)} document chunks.")

    def search(
        self,
        query: str,
        top_k: int = 10,
        where_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search top-k chunks using BM25 scoring with optional metadata filter."""
        self.build_index()
        if not self._bm25 or not self._chunks:
            return []

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        scores = self._bm25.get_scores(query_tokens)

        # Zip scores with chunk objects
        scored_chunks = []
        for idx, score in enumerate(scores):
            if score <= 0:
                continue
            chunk = self._chunks[idx]

            # Apply metadata filter if provided
            if where_filter:
                match = True
                meta = chunk.get("metadata", {})
                for fk, fv in where_filter.items():
                    if meta.get(fk) != fv:
                        match = False
                        break
                if not match:
                    continue

            scored_chunks.append({
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "document_title": chunk["document_title"],
                "section": chunk["section"],
                "text": chunk["text"],
                "score": round(float(score), 4),
                "metadata": chunk.get("metadata", {}),
                "retrieval_source": "bm25_lexical"
            })

        # Sort descending by score
        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        return scored_chunks[:top_k]
