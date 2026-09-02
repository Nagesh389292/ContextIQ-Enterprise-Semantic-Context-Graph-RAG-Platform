"""
ContextIQ — Structure-Aware Semantic Chunker
Splits documents by section headings (`#`, `##`) while preserving metadata and document boundaries.
"""

import re
from typing import Dict, Any, List


class SemanticChunker:
    """Structure-aware chunker splitting text by section boundaries."""

    def chunk_document(self, metadata: Dict[str, Any], body: str) -> List[Dict[str, Any]]:
        """Split document into semantic section chunks with attached metadata."""
        doc_id = metadata.get("document_id", "DOC-000")
        doc_title = metadata.get("title", "Untitled Document")

        # Split by section headings (e.g. ## 1. Overview)
        raw_sections = re.split(r"(^#{1,3}\s+.*$)", body, flags=re.MULTILINE)

        chunks = []
        current_section = "General Overview"
        buffer = []

        chunk_idx = 1
        for part in raw_sections:
            part_str = part.strip()
            if not part_str:
                continue

            if part_str.startswith("#"):
                if buffer:
                    chunk_text = "\n".join(buffer).strip()
                    if len(chunk_text) > 20:
                        chunks.append(self._create_chunk(doc_id, doc_title, current_section, chunk_idx, chunk_text, metadata))
                        chunk_idx += 1
                    buffer = []
                current_section = part_str.lstrip("#").strip()
            else:
                buffer.append(part_str)

        if buffer:
            chunk_text = "\n".join(buffer).strip()
            if len(chunk_text) > 20:
                chunks.append(self._create_chunk(doc_id, doc_title, current_section, chunk_idx, chunk_text, metadata))

        return chunks

    def _create_chunk(
        self,
        doc_id: str,
        doc_title: str,
        section: str,
        chunk_idx: int,
        text: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        chunk_id = f"{doc_id}_CHUNK_{str(chunk_idx).zfill(2)}"
        
        doc_type = metadata.get("document_type", "Document")
        plant_id = metadata.get("plant_id", "")
        machine_id = metadata.get("machine_id", "")
        supplier_id = metadata.get("supplier_id", "")
        process = metadata.get("process", "")

        header_tokens = [f"Document ID: {doc_id}", f"Title: {doc_title}", f"Type: {doc_type}"]
        if plant_id:
            header_tokens.append(f"Plant: {plant_id}")
        if machine_id:
            header_tokens.append(f"Machine: {machine_id}")
        if supplier_id:
            header_tokens.append(f"Supplier: {supplier_id}")
        if process:
            header_tokens.append(f"Process: {process}")
        header_tokens.append(f"Section: {section}")

        header_prefix = f"[{' | '.join(header_tokens)}]\n"
        enriched_text = header_prefix + text

        chunk_metadata = {
            **metadata,
            "chunk_id": chunk_id,
            "document_id": doc_id,
            "document_title": doc_title,
            "section": section,
        }
        return {
            "chunk_id": chunk_id,
            "document_id": doc_id,
            "document_title": doc_title,
            "section": section,
            "text": enriched_text,
            "raw_text": text,
            "metadata": chunk_metadata
        }
