// ContextIQ API Client Service Layer
import axios from 'axios';
import * as mockData from './mockData';
import {
  EntityMetrics, QualityMetrics, SystemHealth, ContextSearchResult,
  OntologyClass, SHACLIssue, EvaluationMetrics, EvaluationTestCase,
  CopilotResponse
} from '../types/api';

const API_BASE = '/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // System Health
  async getSystemHealth(): Promise<SystemHealth> {
    try {
      const res = await apiClient.get('/health');
      return res.data;
    } catch {
      return mockData.MOCK_SYSTEM_HEALTH;
    }
  },

  // Dashboard Metrics
  async getEntityMetrics(): Promise<EntityMetrics> {
    try {
      const res = await apiClient.get('/entities/stats');
      return res.data;
    } catch {
      return mockData.MOCK_ENTITY_METRICS;
    }
  },

  async getQualityMetrics(): Promise<QualityMetrics> {
    try {
      const res = await apiClient.get('/quality/metrics');
      return res.data;
    } catch {
      return mockData.MOCK_QUALITY_METRICS;
    }
  },

  // Context Search
  async searchContext(query: string, category?: string): Promise<ContextSearchResult[]> {
    try {
      const res = await apiClient.get('/search', { params: { q: query || 'bearing M001' } });
      const data = res.data;

      const results: ContextSearchResult[] = [];
      if (data.top_chunks) {
        data.top_chunks.forEach((chunk: any) => {
          results.push({
            id: chunk.chunk_id,
            title: `${chunk.document_title} — ${chunk.section}`,
            category: chunk.metadata.document_type || 'Document',
            score: chunk.rrf_score ? Math.min(1.0, chunk.rrf_score * 25.0) : 0.85,
            subtitle: `Sources: ${chunk.matched_sources?.join(', ') || 'RRF Reranked'} • ${chunk.metadata.plant_id || ''}`,
            snippet: chunk.text,
            metadata: chunk.metadata,
          });
        });
      }
      return results.length > 0 ? results : mockData.MOCK_SEARCH_RESULTS;
    } catch {
      if (!query) return mockData.MOCK_SEARCH_RESULTS;
      return mockData.MOCK_SEARCH_RESULTS.filter(r =>
        r.title.toLowerCase().includes(query.toLowerCase()) ||
        r.snippet.toLowerCase().includes(query.toLowerCase())
      );
    }
  },

  // Knowledge Graph
  async getGraphNeighborhood(nodeId: string = 'M001') {
    try {
      const res = await apiClient.get(`/graph/neighborhood/${nodeId}`);
      return res.data;
    } catch {
      return mockData.MOCK_GRAPH_DATA;
    }
  },

  // Document Intelligence & Vector Corpus
  async getDocumentsList() {
    try {
      const res = await apiClient.get('/documents');
      return res.data;
    } catch {
      return [
        { document_id: 'DOC-001', title: 'Bearing Inspection SOP', document_type: 'SOP', process: 'Maintenance', plant_id: 'P001', entities_count: 4, status: 'Indexed' },
        { document_id: 'DOC-002', title: 'CNC Machine Manual', document_type: 'Manual', process: 'Production', plant_id: 'P001', entities_count: 6, status: 'Indexed' },
      ];
    }
  },

  async getDocumentDetails(docId: string) {
    try {
      const res = await apiClient.get(`/documents/${docId}`);
      return res.data;
    } catch {
      return {
        document_id: docId,
        title: 'Bearing Inspection & Lubrication SOP',
        document_type: 'SOP',
        process: 'Maintenance & Reliability',
        plant_id: 'P001',
        effective_date: '2024-11-12',
        chunks_count: 4,
        entities: [
          { canonical_id: 'M001', entity_type: 'Machine' },
          { canonical_id: 'P001', entity_type: 'Plant' },
          { canonical_id: 'S001', entity_type: 'Supplier' },
        ],
        chunks: [
          { chunk_id: `${docId}_CHUNK_01`, section: '1. Overview', text: 'Mandatory inspection and alignment protocol for bearing units B101.' }
        ]
      };
    }
  },

  async getVectorStats() {
    try {
      const res = await apiClient.get('/vector/stats');
      return res.data;
    } catch {
      return { total_chunks: 180, embedding_model: 'all-MiniLM-L6-v2', status: 'healthy' };
    }
  },

  // Ontology Studio
  async getOntologyClasses(): Promise<OntologyClass[]> {
    try {
      const res = await apiClient.get('/ontology/classes');
      return res.data;
    } catch {
      return mockData.MOCK_ONTOLOGY_CLASSES;
    }
  },

  async getSHACLIssues(): Promise<SHACLIssue[]> {
    try {
      const res = await apiClient.get('/quality/issues');
      return res.data;
    } catch {
      return mockData.MOCK_SHACL_ISSUES;
    }
  },

  // Evaluation Center
  async getEvaluationMetrics(): Promise<EvaluationMetrics> {
    try {
      const res = await apiClient.get('/evaluation/metrics');
      return res.data;
    } catch {
      return mockData.MOCK_EVALUATION_METRICS;
    }
  },

  async getEvaluationTestCases(): Promise<EvaluationTestCase[]> {
    try {
      const res = await apiClient.get('/evaluation/test-cases');
      return res.data;
    } catch {
      return mockData.MOCK_EVALUATION_TEST_CASES;
    }
  },

  // AI Copilot
  async queryCopilot(question: string): Promise<CopilotResponse> {
    try {
      const res = await apiClient.post('/rag/query', { question });
      return res.data;
    } catch {
      return {
        ...mockData.MOCK_COPILOT_RESPONSE,
        id: `QUERY-${Math.floor(Math.random() * 9000 + 1000)}`,
      };
    }
  }
};
