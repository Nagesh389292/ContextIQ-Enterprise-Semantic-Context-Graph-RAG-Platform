import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Terminal, Database, FileText, Cpu, ShieldCheck } from 'lucide-react';
import './CommandPalette.scss';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        isOpen ? onClose() : null;
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const commands = [
    { id: 'copilot', title: 'Open AI Copilot Agent Workspace', route: '/copilot', icon: Cpu, category: 'AI Agent' },
    { id: 'governance', title: 'Data Quality & SHACL Governance', route: '/governance', icon: ShieldCheck, category: 'Governance' },
    { id: 'kg', title: 'Interactive Knowledge Graph Explorer', route: '/knowledge-graph', icon: Database, category: 'Graph' },
    { id: 'docs', title: 'Enterprise Document Intelligence', route: '/documents', icon: FileText, category: 'Documents' },
    { id: 'eval', title: 'Evaluation Framework & Metrics', route: '/evaluation', icon: Terminal, category: 'Benchmark' },
  ];

  const filtered = commands.filter((c) =>
    c.title.toLowerCase().includes(query.toLowerCase()) ||
    c.category.toLowerCase().includes(query.toLowerCase())
  );

  const handleSelect = (route: string) => {
    navigate(route);
    onClose();
  };

  return (
    <div className="command-palette-backdrop" onClick={onClose}>
      <div className="command-palette-modal" onClick={(e) => e.stopPropagation()}>
        <div className="command-palette-input-wrapper">
          <Search size={18} className="search-icon" />
          <input
            type="text"
            placeholder="Type a command or search workspace (Ctrl+K)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
          />
          <kbd className="esc-badge">ESC</kbd>
        </div>
        <div className="command-palette-results">
          {filtered.length === 0 ? (
            <div className="empty-results">No matching commands found.</div>
          ) : (
            filtered.map((c) => {
              const Icon = c.icon;
              return (
                <div key={c.id} className="command-item" onClick={() => handleSelect(c.route)}>
                  <Icon size={16} className="item-icon" />
                  <span className="item-title">{c.title}</span>
                  <span className="item-category">{c.category}</span>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
