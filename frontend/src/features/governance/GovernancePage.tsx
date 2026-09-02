import React, { useState } from 'react';
import { ShieldCheck, AlertTriangle, CheckCircle, Database, GitMerge, FileCode } from 'lucide-react';
import './GovernancePage.scss';

export const GovernancePage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'shacl' | 'lineage' | 'rules'>('shacl');

  const shaclIssues = [
    { id: 'VAL-001', entity: 'Machine M018', type: 'Machine', severity: 'Warning', message: 'Missing installedAt Plant relation', rule: 'sh:minCount 1 on :installedAt' },
    { id: 'VAL-002', entity: 'Machine M024', type: 'Machine', severity: 'Critical', message: 'No active attached sensor found for asset', rule: 'sh:minCount 1 on :hasSensor' },
    { id: 'VAL-003', entity: 'Supplier S018', type: 'Supplier', severity: 'Warning', message: 'Rating 5.4 exceeds maximum allowed 5.0', rule: 'sh:maxInclusive 5.0 on :supplierRating' },
    { id: 'VAL-004', entity: 'Sensor SN142', type: 'Sensor', severity: 'Warning', message: 'Status unknown not in allowed enum', rule: 'sh:in (active faulty calibrating)' }
  ];

  const lineageLayers = [
    { id: 'L1', name: 'Raw Enterprise CSV Ingestion', count: '1,216 Entities', desc: '11 CSV master files & 10,000 telemetry rows' },
    { id: 'L2', name: 'SQL ORM & Relational Schema', count: '1,216 Records', desc: 'SQLAlchemy ORM models with Pydantic v2 schemas' },
    { id: 'L3', name: 'RDFS/OWL Semantic Mapping & SHACL', count: '4 OWL Classes', desc: 'enterprise_ontology.owl & shacl_shapes.ttl' },
    { id: 'L4', name: 'Neo4j Property Knowledge Graph', count: '1,443 Nodes', desc: 'Property graph with 1,135 Cypher edges' },
    { id: 'L5', name: 'ChromaDB Vector Store & BM25 Index', count: '182 Chunks', desc: 'Sentence-transformers embeddings & RRF fusion' }
  ];

  return (
    <div className="governance-page">
      <header className="page-header">
        <div>
          <h1>Enterprise Data Quality & SHACL Governance</h1>
          <p>Automated semantic shape validation, data lineage, and SHACL constraint auditing.</p>
        </div>
        <div className="compliance-badge">
          <ShieldCheck size={20} />
          <span>SHACL Compliance: 95.5%</span>
        </div>
      </header>

      <div className="governance-tabs">
        <button className={activeTab === 'shacl' ? 'active' : ''} onClick={() => setActiveTab('shacl')}>
          <ShieldCheck size={16} /> SHACL Validation Report
        </button>
        <button className={activeTab === 'lineage' ? 'active' : ''} onClick={() => setActiveTab('lineage')}>
          <GitMerge size={16} /> Data Lineage Graph
        </button>
        <button className={activeTab === 'rules' ? 'active' : ''} onClick={() => setActiveTab('rules')}>
          <FileCode size={16} /> Semantic Rules & Shapes
        </button>
      </div>

      {activeTab === 'shacl' && (
        <div className="tab-content">
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="title">Completeness</div>
              <div className="value green">96.4%</div>
            </div>
            <div className="metric-card">
              <div className="title">Consistency</div>
              <div className="value green">95.5%</div>
            </div>
            <div className="metric-card">
              <div className="title">Validity</div>
              <div className="value green">97.2%</div>
            </div>
            <div className="metric-card">
              <div className="title">Uniqueness</div>
              <div className="value green">98.1%</div>
            </div>
          </div>

          <div className="shacl-table-card">
            <h3>Active SHACL Shape Validation Issues</h3>
            <table className="shacl-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Entity</th>
                  <th>Type</th>
                  <th>Severity</th>
                  <th>Violation Message</th>
                  <th>SHACL Rule</th>
                </tr>
              </thead>
              <tbody>
                {shaclIssues.map((issue) => (
                  <tr key={issue.id}>
                    <td><code>{issue.id}</code></td>
                    <td><strong>{issue.entity}</strong></td>
                    <td>{issue.type}</td>
                    <td>
                      <span className={`badge ${issue.severity.toLowerCase()}`}>
                        {issue.severity === 'Critical' ? <AlertTriangle size={12} /> : <CheckCircle size={12} />}
                        {issue.severity}
                      </span>
                    </td>
                    <td>{issue.message}</td>
                    <td><code>{issue.rule}</code></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'lineage' && (
        <div className="tab-content">
          <div className="lineage-container">
            <h3>End-to-End Enterprise Data Lineage</h3>
            <div className="lineage-flow">
              {lineageLayers.map((layer, index) => (
                <div key={layer.id} className="lineage-node">
                  <div className="step-num">Step {index + 1}</div>
                  <div className="node-title">{layer.name}</div>
                  <div className="node-count">{layer.count}</div>
                  <div className="node-desc">{layer.desc}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'rules' && (
        <div className="tab-content">
          <div className="rules-card">
            <h3>SHACL Shapes Definitions (shacl_shapes.ttl)</h3>
            <pre className="ttl-code">
{`:MachineShape a sh:NodeShape ;
    sh:targetClass :Machine ;
    sh:property [
        sh:path :installedAt ;
        sh:minCount 1 ;
        sh:class :Plant ;
        sh:message "Machine must be installed at exactly 1 Plant." ;
    ] ;
    sh:property [
        sh:path :hasSensor ;
        sh:minCount 1 ;
        sh:class :Sensor ;
        sh:message "Machine must have at least 1 active Sensor attached." ;
    ] .`}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};
