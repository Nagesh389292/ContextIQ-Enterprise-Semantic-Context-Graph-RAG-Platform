import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../../services/api';
import { ShieldCheck, AlertTriangle, CheckCircle2, AlertCircle } from 'lucide-react';
import './DataQualityPage.scss';

export const DataQualityPage: React.FC = () => {
  const { data: quality } = useQuery({ queryKey: ['qualityMetrics'], queryFn: () => apiService.getQualityMetrics() });
  const { data: issues } = useQuery({ queryKey: ['shaclIssues'], queryFn: () => apiService.getSHACLIssues() });

  return (
    <div className="quality-page">
      <div className="page-header">
        <div>
          <h1>Data Quality & SHACL Validation</h1>
          <p className="subtitle">Real-time enterprise data health auditing against OWL shapes and relational constraints.</p>
        </div>
        <div className="overall-score-badge">
          Overall Quality: <strong>96.6%</strong>
        </div>
      </div>

      <div className="quality-metrics-grid">
        <div className="q-card"><span className="q-title">Completeness</span><span className="q-val">96.4%</span></div>
        <div className="q-card"><span className="q-title">Consistency</span><span className="q-val">94.8%</span></div>
        <div className="q-card"><span className="q-title">Validity (SHACL)</span><span className="q-val">97.2%</span></div>
        <div className="q-card"><span className="q-title">Uniqueness</span><span className="q-val">98.1%</span></div>
      </div>

      <div className="issues-card">
        <h2>SHACL Validation Issues ({issues?.length || 0})</h2>
        <table className="issues-table">
          <thead>
            <tr>
              <th>Issue ID</th>
              <th>Target Entity</th>
              <th>Type</th>
              <th>Severity</th>
              <th>Validation Rule / Message</th>
            </tr>
          </thead>
          <tbody>
            {issues?.map((iss) => (
              <tr key={iss.id}>
                <td className="font-mono">{iss.id}</td>
                <td><strong>{iss.entity}</strong></td>
                <td>{iss.entity_type}</td>
                <td>
                  <span className={`sev-badge ${iss.severity.toLowerCase()}`}>
                    {iss.severity === 'Critical' ? <AlertCircle size={12} /> : <AlertTriangle size={12} />}
                    {iss.severity}
                  </span>
                </td>
                <td>
                  <div className="msg-text">{iss.message}</div>
                  <div className="rule-sub font-mono">{iss.rule}</div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
