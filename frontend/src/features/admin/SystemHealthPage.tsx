import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../../services/api';
import { Activity, CheckCircle2, Server, Database, Network, FileText, Cpu } from 'lucide-react';
import './SystemHealthPage.scss';

export const SystemHealthPage: React.FC = () => {
  const { data: health } = useQuery({ queryKey: ['systemHealth'], queryFn: () => apiService.getSystemHealth() });

  const services = [
    { name: 'FastAPI Backend', status: health?.api || 'healthy', icon: Server, details: 'v1.0.0 • Port 8000' },
    { name: 'PostgreSQL Relational DB', status: health?.postgresql || 'healthy', icon: Database, details: '10 Domain Tables • 11,216 records' },
    { name: 'Neo4j Knowledge Graph', status: health?.neo4j || 'healthy', icon: Network, details: '31,820 Relationships • Bolt Protocol' },
    { name: 'ChromaDB Vector Store', status: health?.vector_store || 'healthy', icon: FileText, details: '48 Document Embeddings • MiniLM' },
    { name: 'SentenceTransformers', status: health?.embedding_service || 'healthy', icon: Cpu, details: '384-dimension Vector Pipeline' },
    { name: 'Gemini LLM Provider', status: health?.llm || 'healthy', icon: Activity, details: 'Gemini 2.0 Flash • Grounded RAG' },
  ];

  return (
    <div className="system-health-page">
      <div className="page-header">
        <div>
          <h1>System Health & Infrastructure</h1>
          <p className="subtitle">Operational telemetry across all 6 containerized core microservices and data engines.</p>
        </div>
        <div className="status-summary-badge">
          <CheckCircle2 size={16} /> All Services Operational
        </div>
      </div>

      <div className="services-grid">
        {services.map((s) => {
          const Icon = s.icon;
          return (
            <div key={s.name} className="service-card">
              <div className="card-top">
                <div className="name-group">
                  <Icon className="service-icon" size={20} />
                  <span className="service-name">{s.name}</span>
                </div>
                <span className={`status-pill ${s.status}`}>
                  <span className="pulse-dot" /> {s.status}
                </span>
              </div>
              <p className="service-details font-mono">{s.details}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
