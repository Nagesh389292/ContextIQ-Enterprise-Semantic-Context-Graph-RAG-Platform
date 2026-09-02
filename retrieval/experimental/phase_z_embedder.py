"""
Phase Z — Experimental Isolated Embedder Module
Loads and evaluates fine-tuned dense embedding checkpoints in isolation without touching production embedder.
"""

import os
import numpy as np
from pathlib import Path
from typing import List, Union
from loguru import logger
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EXPERIMENTAL_CHECKPOINT_DIR = PROJECT_ROOT / "artifacts" / "phase_z" / "checkpoint"

class PhaseZExperimentalEmbedder:
    """Isolated experimental embedding model for Phase Z offline evaluation."""

    def __init__(self, checkpoint_path: Union[str, Path] = None):
        if checkpoint_path is not None:
            self.model_path = str(checkpoint_path)
        elif EXPERIMENTAL_CHECKPOINT_DIR.exists() and (EXPERIMENTAL_CHECKPOINT_DIR / "config.json").exists():
            self.model_path = str(EXPERIMENTAL_CHECKPOINT_DIR)
        else:
            self.model_path = "sentence-transformers/all-MiniLM-L6-v2"

        logger.info(f"Initializing PhaseZExperimentalEmbedder with model path: {self.model_path}")
        self.model = SentenceTransformer(self.model_path)

    def encode(self, texts: Union[str, List[str]], convert_to_numpy: bool = True) -> Union[np.ndarray, List[np.ndarray]]:
        """Encode text or list of texts into dense vectors."""
        return self.model.encode(texts, convert_to_numpy=convert_to_numpy)

    def compute_cosine_sim(self, text_a: str, text_b: str) -> float:
        """Compute cosine similarity between two texts."""
        v_a = self.encode(text_a)
        v_b = self.encode(text_b)
        norm_a = np.linalg.norm(v_a)
        norm_b = np.linalg.norm(v_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(v_a, v_b) / (norm_a * norm_b))
