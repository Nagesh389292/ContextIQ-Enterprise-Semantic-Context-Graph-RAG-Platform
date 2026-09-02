import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../../services/api';
import { FileText, Upload, Search, CheckCircle2, Tag, Layers, Cpu } from 'lucide-react';
import './DocumentsPage.scss';

export const DocumentsPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDocId, setSelectedDocId] = useState<string>('DOC-001');

  // Live Query for Documents List
  const { data: docsList, isLoading } = useQuery({
    queryKey: ['documentsList'],
    queryFn: () => apiService.getDocumentsList(),
  });

  // Live Query for Selected Document Details
  const { data: docDetail } = useQuery({
    queryKey: ['documentDetail', selectedDocId],
    queryFn: () => apiService.getDocumentDetails(selectedDocId),
    enabled: Boolean(selectedDocId),
  });

  // Live Vector Stats
  const { data: vectorStats } = useQuery({
    queryKey: ['vectorStats'],
    queryFn: () => apiService.getVectorStats(),
  });

  const filteredDocs = docsList?.filter((d: any) =>
    d.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    d.document_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
    d.process.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="documents-page">
      <div className="page-header">
        <div>
          <h1>Enterprise Knowledge Base</h1>
          <p className="subtitle">
            {vectorStats?.total_chunks || 180} chunks indexed in persistent ChromaDB vector store ({vectorStats?.embedding_model || 'all-MiniLM-L6-v2'}).
          </p>
        </div>
        <button className="upload-btn">
          <Upload size={16} /> Upload Enterprise Document
        </button>
      </div>

      <div className="docs-search-bar">
        <Search size={16} className="search-icon" />
        <input
          type="text"
          placeholder="Filter documents by title, type, process, plant..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="docs-layout">
        {/* Document Table */}
        <div className="docs-table-card">
          <div className="table-header font-mono">
            <span>Enterprise Documents Corpus ({filteredDocs?.length || 0})</span>
          </div>

          {isLoading ? (
            <div className="p-4"><div className="skeleton" style={{ height: '120px' }} /></div>
          ) : (
            <table className="docs-table">
              <thead>
                <tr>
                  <th>Document Title</th>
                  <th>Type</th>
                  <th>Process</th>
                  <th>Plant</th>
                  <th>Extracted Entities</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {filteredDocs?.map((doc: any) => (
                  <tr
                    key={doc.document_id}
                    className={selectedDocId === doc.document_id ? 'active' : ''}
                    onClick={() => setSelectedDocId(doc.document_id)}
                  >
                    <td className="doc-title-cell">
                      <FileText size={16} className="doc-icon" />
                      <span>{doc.title}</span>
                    </td>
                    <td><span className="type-badge">{doc.document_type}</span></td>
                    <td>{doc.process}</td>
                    <td><span className="plant-tag font-mono">{doc.plant_id}</span></td>
                    <td><strong>{doc.entities_count}</strong> entities</td>
                    <td><span className="status-badge"><CheckCircle2 size={12} /> {doc.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Selected Document Details Drawer */}
        <aside className="doc-detail-drawer">
          {docDetail ? (
            <>
              <div className="drawer-header">
                <h2>{docDetail.title}</h2>
                <span className="doc-id">{docDetail.document_id} • Effective {docDetail.effective_date}</span>
              </div>

              <div className="drawer-section">
                <h3>Metadata</h3>
                <div className="meta-row"><span>Document Type</span><strong>{docDetail.document_type}</strong></div>
                <div className="meta-row"><span>Business Process</span><strong>{docDetail.process}</strong></div>
                <div className="meta-row"><span>Plant Facility</span><strong>{docDetail.plant_id}</strong></div>
                <div className="meta-row"><span>Section Chunks</span><strong>{docDetail.chunks_count} chunks</strong></div>
                <div className="meta-row"><span>Vector Store</span><strong>ChromaDB (384-dim)</strong></div>
              </div>

              <div className="drawer-section">
                <h3><Tag size={14} /> Extracted & Graph-Linked Entities</h3>
                <div className="chips-list">
                  {docDetail.entities?.map((e: any, idx: number) => (
                    <span key={idx} className="chip font-mono">
                      <Tag size={10} /> {e.canonical_id} ({e.entity_type})
                    </span>
                  ))}
                </div>
              </div>

              <div className="drawer-section">
                <h3><Layers size={14} /> Sample Semantic Section Chunks</h3>
                <div className="chunks-list">
                  {docDetail.chunks?.slice(0, 3).map((chunk: any) => (
                    <div key={chunk.chunk_id} className="chunk-card">
                      <div className="chunk-head font-mono">{chunk.section}</div>
                      <p className="chunk-snippet">{chunk.text.substring(0, 140)}...</p>
                    </div>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="empty-state">Select a document to inspect metadata and semantic section chunks.</div>
          )}
        </aside>
      </div>
    </div>
  );
};
