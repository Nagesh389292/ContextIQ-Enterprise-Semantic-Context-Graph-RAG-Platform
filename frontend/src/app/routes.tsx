import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AppShell } from '../components/layout/AppShell';

import { DashboardPage } from '../features/dashboard/DashboardPage';
import { ContextExplorerPage } from '../features/context/ContextExplorerPage';
import { KnowledgeGraphPage } from '../features/knowledgeGraph/KnowledgeGraphPage';
import { OntologyStudioPage } from '../features/ontology/OntologyStudioPage';
import { DocumentsPage } from '../features/documents/DocumentsPage';
import { AICopilotPage } from '../features/copilot/AICopilotPage';
import { ProcessesPage } from '../features/processes/ProcessesPage';
import { DataQualityPage } from '../features/quality/DataQualityPage';
import { GovernancePage } from '../features/governance/GovernancePage';
import { EvaluationPage } from '../features/evaluation/EvaluationPage';
import { SystemHealthPage } from '../features/admin/SystemHealthPage';
import { LoginPage } from '../features/auth/LoginPage';

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      {/* Main Authenticated Layout Shell */}
      <Route
        path="/*"
        element={
          <AppShell>
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/context" element={<ContextExplorerPage />} />
              <Route path="/graph" element={<KnowledgeGraphPage />} />
              <Route path="/ontology" element={<OntologyStudioPage />} />
              <Route path="/documents" element={<DocumentsPage />} />
              <Route path="/copilot" element={<AICopilotPage />} />
              <Route path="/processes" element={<ProcessesPage />} />
              <Route path="/quality" element={<GovernancePage />} />
              <Route path="/governance" element={<GovernancePage />} />
              <Route path="/evaluation" element={<EvaluationPage />} />
              <Route path="/system" element={<SystemHealthPage />} />
              <Route path="/settings" element={<Navigate to="/system" replace />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </AppShell>
        }
      />
    </Routes>
  );
};
