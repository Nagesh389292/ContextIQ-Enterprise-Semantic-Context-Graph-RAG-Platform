"""
ContextIQ — Document Loader
Idempotent document loader parsing JSON frontmatter and document body.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from loguru import logger

RAW_DIR = Path(__file__).parent.parent / "raw"


class DocumentLoader:
    """Loads raw document files and extracts metadata headers and body content."""

    def __init__(self, raw_dir: Path | None = None):
        self.raw_dir = raw_dir or RAW_DIR

    def load_document(self, file_path: Path) -> Tuple[Dict[str, Any], str]:
        """Parse frontmatter JSON metadata block and raw markdown body."""
        text = file_path.read_text(encoding="utf-8")

        # Match ```json ... ``` block
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            try:
                metadata = json.loads(match.group(1))
            except Exception as e:
                logger.warning(f"Error parsing metadata in {file_path.name}: {e}")
                metadata = {"document_id": file_path.stem, "title": file_path.stem}
            body = text[match.end():].strip()
        else:
            metadata = {"document_id": file_path.stem, "title": file_path.stem}
            body = text.strip()

        return metadata, body

    def load_all(self) -> List[Tuple[Dict[str, Any], str]]:
        """Load all documents from raw directory."""
        if not self.raw_dir.exists():
            return []

        docs = []
        for file in sorted(self.raw_dir.glob("*.md")):
            docs.append(self.load_document(file))
        return docs
