import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../../services/api';
import { Box, Code, Download, ShieldCheck, CheckCircle2, FileCode } from 'lucide-react';
import './OntologyStudioPage.scss';

export const OntologyStudioPage: React.FC = () => {
  const { data: classes } = useQuery({
    queryKey: ['ontologyClasses'],
    queryFn: () => apiService.getOntologyClasses(),
  });

  const [selectedClass, setSelectedClass] = useState<string>('Machine');

  const currentClassDetails = classes?.find((c) => c.name === selectedClass) || classes?.[0];

  return (
    <div className="ontology-studio-page">
      <div className="page-header">
        <div>
          <h1>Ontology Studio</h1>
          <p className="subtitle">Enterprise Manufacturing OWL/RDF Semantic Schema & SHACL Constraint Specifications.</p>
        </div>
        <button className="download-btn">
          <Download size={16} /> Export Turtle (.ttl)
        </button>
      </div>

      <div className="studio-layout">
        {/* Left Column: OWL Classes List */}
        <div className="classes-panel">
          <div className="panel-header">
            <Box size={16} className="panel-icon" />
            <span>OWL Classes ({classes?.length || 0})</span>
          </div>
          <div className="class-list">
            {classes?.map((c) => (
              <button
                key={c.name}
                className={`class-item ${selectedClass === c.name ? 'active' : ''}`}
                onClick={() => setSelectedClass(c.name)}
              >
                <div className="class-info">
                  <span className="class-name">{c.name}</span>
                  <span className="class-sub">{c.superClass ? `subClassOf ${c.superClass}` : 'EnterpriseResource'}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Right Column: Class Inspector & Specifications */}
        <div className="inspector-panel">
          {currentClassDetails ? (
            <>
              <div className="class-header">
                <h2>{currentClassDetails.name}</h2>
                <span className="class-uri font-mono">{currentClassDetails.class}</span>
                <p className="class-desc">{currentClassDetails.comment}</p>
              </div>

              <div className="specs-grid">
                {/* Datatype Properties */}
                <div className="spec-card">
                  <h3>Datatype Properties (Attributes)</h3>
                  <div className="prop-tags">
                    {currentClassDetails.datatype_properties?.map((p) => (
                      <span key={p} className="prop-tag dt">{p}</span>
                    ))}
                  </div>
                </div>

                {/* Object Properties */}
                <div className="spec-card">
                  <h3>Object Properties (Relationships)</h3>
                  <div className="prop-tags">
                    {currentClassDetails.object_properties?.map((p) => (
                      <span key={p} className="prop-tag obj">{p}</span>
                    ))}
                  </div>
                </div>

                {/* SHACL Constraints */}
                <div className="spec-card full-width">
                  <h3><ShieldCheck size={16} className="shacl-icon" /> SHACL Property Shape Constraints</h3>
                  <div className="shacl-list">
                    {currentClassDetails.shacl_constraints?.map((rule, i) => (
                      <div key={i} className="shacl-rule font-mono">
                        <CheckCircle2 size={14} className="rule-icon" /> {rule}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="empty-state">Select an OWL class to inspect properties and SHACL shapes.</div>
          )}
        </div>
      </div>
    </div>
  );
};
