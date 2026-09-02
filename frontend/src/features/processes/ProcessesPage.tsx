import React, { useState } from 'react';
import { GitMerge, ArrowRight, CheckCircle2, Factory, ShieldCheck, Box } from 'lucide-react';
import './ProcessesPage.scss';

export const ProcessesPage: React.FC = () => {
  const [selectedProcess, setSelectedProcess] = useState('Plan-to-Produce');

  const processes = [
    { name: 'Plan-to-Produce', desc: 'End-to-end manufacturing workflow from demand planning to finished assembly.', steps: ['Demand Plan', 'Production Order', 'Material Allocation', 'Machine Assembly', 'Quality Inspection', 'Finished Product'] },
    { name: 'Maintenance & Reliability', desc: 'Predictive & corrective maintenance triggering technician SOP actions.', steps: ['Sensor Anomaly', 'Event Trigger', 'Technician Assigned', 'Parts Replacements', 'SOP Verification', 'Machine Restored'] },
    { name: 'Procure-to-Pay', desc: 'Material supply chain sourcing from Tier 1..3 suppliers.', steps: ['Requisition', 'Purchase Order', 'Supplier Delivery', 'Quality Audit', 'Material Staging', 'Payment Settlement'] },
  ];

  const activeP = processes.find(p => p.name === selectedProcess) || processes[0];

  return (
    <div className="processes-page">
      <div className="page-header">
        <h1>Business Process Explorer</h1>
        <p className="subtitle">Semantic business process models mapping SAP-style workflows to underlying knowledge graph entities.</p>
      </div>

      <div className="process-selector-row">
        {processes.map(p => (
          <button
            key={p.name}
            className={`process-card-btn ${selectedProcess === p.name ? 'active' : ''}`}
            onClick={() => setSelectedProcess(p.name)}
          >
            <GitMerge size={20} className="p-icon" />
            <div className="p-text">
              <h3>{p.name}</h3>
              <p>{p.desc}</p>
            </div>
          </button>
        ))}
      </div>

      <div className="flow-diagram-card">
        <h2>{activeP.name} Flow Map</h2>
        <div className="flow-steps-container">
          {activeP.steps.map((step, idx) => (
            <React.Fragment key={step}>
              <div className="flow-step-node">
                <span className="step-num">Step {idx + 1}</span>
                <span className="step-name">{step}</span>
              </div>
              {idx < activeP.steps.length - 1 && <ArrowRight className="flow-arrow" size={18} />}
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
};
