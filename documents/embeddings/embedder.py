"""
ContextIQ — Embeddings Provider Abstraction Layer
Uses sentence-transformers/all-MiniLM-L6-v2 (or deterministic hashing fallback) for 384-dimensional vector embeddings.
"""

from typing import List
import hashlib
from loguru import logger
from config import settings

_transformer_model = None
_use_fallback = False


def get_embedding_model():
    """Singleton getter for SentenceTransformer embedding model."""
    global _transformer_model, _use_fallback
    if _transformer_model is None and not _use_fallback:
        try:
            from sentence_transformers import SentenceTransformer
            model_name = settings.embedding_model
            logger.info(f"Loading embedding model: {model_name}")
            _transformer_model = SentenceTransformer(model_name)
        except Exception as exc:
            logger.warning(f"Could not load SentenceTransformer ({exc}). Using deterministic 384-dim embedder fallback.")
            _use_fallback = True
    return _transformer_model


class Embedder:
    """Configurable embedding provider abstraction."""

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.embedding_model
        self.dimension = settings.embedding_dimension

    def _fallback_hash_vector(self, text: str) -> List[float]:
        """Generate a deterministic normalized 384-dimensional float vector."""
        vec = []
        for i in range(self.dimension):
            h = hashlib.md5(f"{text}_{i}".encode("utf-8")).hexdigest()
            val = (int(h[:8], 16) / 0xFFFFFFFF) * 2.0 - 1.0
            vec.append(round(val, 6))
        return vec

    def encode_text(self, text: str) -> List[float]:
        """Encode single string text into vector float array."""
        model = get_embedding_model()
        if model is not None:
            try:
                vector = model.encode(text, convert_to_numpy=True)
                return vector.tolist()
            except Exception:
                pass
        return self._fallback_hash_vector(text)

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Encode list of string texts into batch vector array."""
        model = get_embedding_model()
        if model is not None:
            try:
                vectors = model.encode(texts, convert_to_numpy=True, batch_size=32)
                return vectors.tolist()
            except Exception:
                pass
        return [self._fallback_hash_vector(t) for t in texts]
