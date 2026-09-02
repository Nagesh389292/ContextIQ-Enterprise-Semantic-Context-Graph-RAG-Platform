import React, { useState, useCallback } from 'react';
import ReactFlow, {
  Controls, Background, useNodesState, useEdgesState,
  MarkerType, Node, Edge
} from 'reactflow';
import 'reactflow/dist/style.css';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../../services/api';
import { Network, Search, X, Info, ChevronRight, Layers } from 'lucide-react';
import './KnowledgeGraphPage.scss';

const INITIAL_NODES: Node[] = [
  { id: 'P001', data: { label: 'Northgate Plant (P001)' }, position: { x: 250, y: 50 }, style: { background: '#1E3A8A', color: '#fff', border: '1px solid #3B82F6', borderRadius: 8, padding: 10 } },
  { id: 'L001', data: { label: 'Assembly Line A (L001)' }, position: { x: 250, y: 160 }, style: { background: '#1F2937', color: '#fff', border: '1px solid #4B5563', borderRadius: 8, padding: 10 } },
  { id: 'M001', data: { label: 'CNC Machine M001' }, position: { x: 250, y: 270 }, style: { background: '#2563EB', color: '#fff', border: '1px solid #60A5FA', borderRadius: 8, padding: 12, fontWeight: 'bold' } },
  { id: 'SN001', data: { label: 'Temp Sensor SN001' }, position: { x: 50, y: 390 }, style: { background: '#065F46', color: '#fff', border: '1px solid #10B981', borderRadius: 8, padding: 10 } },
  { id: 'SN002', data: { label: 'Vibration Sensor SN002' }, position: { x: 250, y: 390 }, style: { background: '#065F46', color: '#fff', border: '1px solid #10B981', borderRadius: 8, padding: 10 } },
  { id: 'S001', data: { label: 'Supplier S001' }, position: { x: 480, y: 270 }, style: { background: '#5B21B6', color: '#fff', border: '1px solid #8B5CF6', borderRadius: 8, padding: 10 } },
  { id: 'MAT001', data: { label: 'Bearing B101' }, position: { x: 480, y: 390 }, style: { background: '#7C2D12', color: '#fff', border: '1px solid #F97316', borderRadius: 8, padding: 10 } },
];

const INITIAL_EDGES: Edge[] = [
  { id: 'e1', source: 'L001', target: 'P001', label: 'LOCATED_AT', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e2', source: 'M001', target: 'L001', label: 'ON_LINE', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e3', source: 'M001', target: 'P001', label: 'INSTALLED_AT', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e4', source: 'SN001', target: 'M001', label: 'ATTACHED_TO', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e5', source: 'SN002', target: 'M001', label: 'ATTACHED_TO', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e6', source: 'M001', target: 'S001', label: 'SUPPLIED_BY', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e7', source: 'S001', target: 'MAT001', label: 'SUPPLIES', markerEnd: { type: MarkerType.ArrowClosed } },
];

export const KnowledgeGraphPage: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(INITIAL_NODES);
  const [edges, setEdges, onEdgesChange] = useEdgesState(INITIAL_EDGES);
  const [selectedNode, setSelectedNode] = useState<Node | null>(INITIAL_NODES[2]); // Machine M001 default

  const onNodeClick = useCallback((_: any, node: Node) => {
    setSelectedNode(node);
  }, []);

  return (
    <div className="kg-explorer-page">
      <div className="page-header">
        <div>
          <h1>Knowledge Graph Explorer</h1>
          <p className="subtitle">Interactive Neo4j graph visualization across enterprise assets, suppliers, sensors, and orders.</p>
        </div>
        <div className="graph-stats-badge">
          <span>Nodes: <strong>12,450</strong></span>
          <span className="dot">•</span>
          <span>Edges: <strong>31,820</strong></span>
        </div>
      </div>

      <div className="graph-content-wrapper">
        <div className="graph-canvas-container">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={onNodeClick}
            fitView
          >
            <Background color="#374151" gap={16} />
            <Controls />
          </ReactFlow>
        </div>

        {/* Node Inspector Right Drawer */}
        {selectedNode && (
          <aside className="node-inspector">
            <div className="inspector-header">
              <div className="title-group">
                <Info size={18} className="info-icon" />
                <span>Entity Inspector</span>
              </div>
              <button className="close-btn" onClick={() => setSelectedNode(null)}>
                <X size={16} />
              </button>
            </div>

            <div className="inspector-body">
              <div className="entity-main font-mono">
                <h2>{selectedNode.data.label}</h2>
                <span className="entity-id">ID: {selectedNode.id}</span>
              </div>

              <div className="props-section">
                <h3>Entity Properties</h3>
                <div className="prop-row"><span className="prop-name">Type</span><span className="prop-val">CNC Machine</span></div>
                <div className="prop-row"><span className="prop-name">Plant</span><span className="prop-val">Northgate Plant (P001)</span></div>
                <div className="prop-row"><span className="prop-name">Status</span><span className="prop-val status-op">Operational</span></div>
                <div className="prop-row"><span className="prop-name">Attached Sensors</span><span className="prop-val">2 (SN001, SN002)</span></div>
                <div className="prop-row"><span className="prop-name">Supplier</span><span className="prop-val">Precision Bearings Inc (S001)</span></div>
              </div>

              <div className="relationships-section">
                <h3>Graph Relationships (Cypher)</h3>
                <div className="rel-card">
                  <span className="rel-type">HAS_SENSOR</span>
                  <span className="rel-target">SN001, SN002</span>
                </div>
                <div className="rel-card">
                  <span className="rel-type">SUPPLIED_BY</span>
                  <span className="rel-target">Supplier S001</span>
                </div>
                <div className="rel-card">
                  <span className="rel-type">INSTALLED_AT</span>
                  <span className="rel-target">Plant P001</span>
                </div>
              </div>
            </div>
          </aside>
        )}
      </div>
    </div>
  );
};
