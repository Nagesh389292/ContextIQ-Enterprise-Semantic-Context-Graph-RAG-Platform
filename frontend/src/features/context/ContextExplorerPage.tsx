import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../../services/api';
import { Search, Filter, Database, ArrowRight, FileText, Network, GitMerge, Layers } from 'lucide-react';
import './ContextExplorerPage.scss';

export const ContextExplorerPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState<string>('All');

  const { data: searchResults, isLoading } = useQuery({
    queryKey: ['contextSearch', searchTerm, activeCategory],
    queryFn: () => apiService.searchContext(searchTerm, activeCategory === 'All' ? undefined : activeCategory),
  });

  const categories = ['All', 'Entity', 'Relationship', 'Document', 'Process'];

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Entity': return <Database size={16} className="cat-icon entity" />;
      case 'Relationship': return <Network size={16} className="cat-icon rel" />;
      case 'Document': return <FileText size={16} className="cat-icon doc" />;
      case 'Process': return <GitMerge size={16} className="cat-icon proc" />;
      default: return <Layers size={16} className="cat-icon default" />;
    }
  };

  return (
    <div className="context-explorer-page">
      <div className="page-header">
        <h1>Context Explorer</h1>
        <p className="subtitle">Perform hybrid semantic queries across structured enterprise data, graph relationships, and documents.</p>
      </div>

      <div className="search-bar-card">
        <div className="search-input-group">
          <Search className="search-icon" size={20} />
          <input
            type="text"
            placeholder="Search context e.g. machine M001, supplier S001, bearing SOP, production order..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="category-filters">
          <Filter size={14} className="filter-icon" />
          {categories.map((cat) => (
            <button
              key={cat}
              className={`filter-btn ${activeCategory === cat ? 'active' : ''}`}
              onClick={() => setActiveCategory(cat)}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      <div className="results-container">
        <div className="results-header">
          <h2>Semantic Search Results ({searchResults?.length || 0})</h2>
          <span className="results-info">Grounded across PostgreSQL & Neo4j</span>
        </div>

        {isLoading ? (
          <div className="loading-state">
            <div className="skeleton" style={{ height: '80px', marginBottom: '12px' }} />
            <div className="skeleton" style={{ height: '80px', marginBottom: '12px' }} />
          </div>
        ) : (
          <div className="results-list">
            {searchResults?.map((item) => (
              <div key={item.id} className="result-card">
                <div className="card-top">
                  <div className="title-group">
                    {getCategoryIcon(item.category)}
                    <span className="result-title">{item.title}</span>
                    <span className={`category-tag ${item.category.toLowerCase()}`}>{item.category}</span>
                  </div>
                  <span className="score-badge">Match: {Math.round(item.score * 100)}%</span>
                </div>
                <div className="result-subtitle">{item.subtitle}</div>
                <p className="result-snippet">{item.snippet}</p>
                <div className="card-bottom">
                  <div className="meta-tags">
                    {Object.entries(item.metadata).map(([k, v]) => (
                      <span key={k} className="meta-tag">{k}: <strong>{String(v)}</strong></span>
                    ))}
                  </div>
                  <button className="inspect-btn">
                    Inspect Context <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
