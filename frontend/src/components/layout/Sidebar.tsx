import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, Search, Network, Box, FileText,
  Bot, GitMerge, ShieldCheck, BarChart3, Activity, Settings
} from 'lucide-react';
import './Sidebar.scss';

interface NavItem {
  path: string;
  label: string;
  icon: React.ElementType;
  badge?: string;
}

const NAV_ITEMS: NavItem[] = [
  { path: '/', label: 'Overview', icon: LayoutDashboard },
  { path: '/context', label: 'Context Explorer', icon: Search },
  { path: '/graph', label: 'Knowledge Graph', icon: Network, badge: 'Neo4j' },
  { path: '/ontology', label: 'Ontology Studio', icon: Box, badge: 'OWL' },
  { path: '/documents', label: 'Enterprise Knowledge', icon: FileText },
  { path: '/copilot', label: 'AI Copilot', icon: Bot, badge: 'Hybrid' },
  { path: '/processes', label: 'Business Processes', icon: GitMerge },
  { path: '/quality', label: 'Data Quality & SHACL', icon: ShieldCheck },
  { path: '/evaluation', label: 'AI Evaluation', icon: BarChart3 },
  { path: '/system', label: 'System Health', icon: Activity },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="app-sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo">
          <div className="logo-hex">◈</div>
          <span className="brand-name">ContextIQ</span>
        </div>
        <span className="brand-tag">v1.0 • Enterprise</span>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">PLATFORM</div>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon className="nav-icon" size={18} />
              <span className="nav-label">{item.label}</span>
              {item.badge && <span className="nav-badge">{item.badge}</span>}
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <NavLink to="/settings" className="nav-item">
          <Settings size={18} />
          <span>Settings</span>
        </NavLink>
      </div>
    </aside>
  );
};
