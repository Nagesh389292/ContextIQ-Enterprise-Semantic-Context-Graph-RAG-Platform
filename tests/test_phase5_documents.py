"""
Phase 5 tests — Enterprise Document Intelligence, Graph Linking, and Vector Corpus (ChromaDB).
"""

from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from documents.loaders.doc_loader import DocumentLoader
from documents.chunking.semantic_chunker import SemanticChunker
from documents.entity_linking.graph_linker import GraphLinker
from documents.embeddings.embedder import Embedder
from documents.indexing.vector_store import VectorStore
from documents.service import DocumentService
from api.main import app

client = TestClient(app)
ROOT = Path(__file__).parent.parent


class TestDocumentCorpusAndLoader:

    def test_corpus_files_exist(self):
        raw_dir = ROOT / "documents" / "raw"
        assert raw_dir.exists()
        files = list(raw_dir.glob("*.md"))
        assert len(files) >= 40

    def test_loader_parses_metadata(self):
        loader = DocumentLoader()
        docs = loader.load_all()
        assert len(docs) >= 40
        metadata, body = docs[0]
        assert "document_id" in metadata
        assert "plant_id" in metadata
        assert len(body) > 50


class TestSemanticChunkingAndLinking:

    def test_structure_aware_chunking(self):
        loader = DocumentLoader()
        chunker = SemanticChunker()
        docs = loader.load_all()
        metadata, body = docs[0]
        chunks = chunker.chunk_document(metadata, body)
        assert len(chunks) >= 2
        first_chunk = chunks[0]
        assert "chunk_id" in first_chunk
        assert "section" in first_chunk
        assert first_chunk["metadata"]["plant_id"] == metadata.get("plant_id")

    def test_entity_extraction_from_text(self):
        linker = GraphLinker()
        text = "Machine M001 at Plant P001 requires bearing B101 from Supplier S001. Sensor SN001 monitors temperature."
        metadata = {"machine_id": "M001", "plant_id": "P001"}
        entities = linker.extract_entities(text, metadata)
        assert len(entities) >= 3
        ids = [e["canonical_id"] for e in entities]
        assert "M001" in ids
        assert "P001" in ids
        assert "S001" in ids


class TestVectorStoreAndEmbeddings:

    def test_embedder_dimension(self):
        embedder = Embedder()
        vec = embedder.encode_text("Test embedding query")
        assert len(vec) == 384

    def test_vector_store_upsert_and_search(self):
        persist_path = ROOT / "data" / "test_chroma_db"
        store = VectorStore(persist_dir=str(persist_path), collection_name="test_corpus_unit")
        sample_chunks = [
            {
                "chunk_id": "TEST_DOC_CHUNK_01",
                "text": "CNC Machine M001 temperature threshold is 85.0 degree celsius.",
                "metadata": {"document_id": "TEST_DOC", "plant_id": "P001", "document_type": "Manual"}
            },
            {
                "chunk_id": "TEST_DOC_CHUNK_02",
                "text": "Hydraulic press pressure safety protocol at Plant P002.",
                "metadata": {"document_id": "TEST_DOC_2", "plant_id": "P002", "document_type": "Safety"}
            }
        ]
        store.add_chunks(sample_chunks)
        assert store.get_stats()["total_chunks"] >= 2

        # Similarity search
        results = store.search("temperature threshold M001", top_k=1)
        assert len(results) == 1
        assert results[0]["chunk_id"] == "TEST_DOC_CHUNK_01"
        assert results[0]["score"] >= 0.0

        # Metadata filter search
        filtered = store.search("protocol", top_k=2, where_filter={"plant_id": "P002"})
        assert len(filtered) == 1
        assert filtered[0]["chunk_id"] == "TEST_DOC_CHUNK_02"


class TestDocumentAPIRoutes:

    def test_list_documents(self):
        res = client.get("/api/v1/documents")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert len(data) >= 40
        assert "document_id" in data[0]

    def test_get_document_detail(self):
        res = client.get("/api/v1/documents/DOC-001")
        assert res.status_code == 200
        data = res.json()
        assert data["document_id"] == "DOC-001"
        assert "entities" in data
        assert "chunks" in data

    def test_search_documents_vector(self):
        res = client.get("/api/v1/documents/search?q=bearing+overheating")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)

    def test_get_vector_stats(self):
        res = client.get("/api/v1/vector/stats")
        assert res.status_code == 200
        data = res.json()
        assert "total_chunks" in data
