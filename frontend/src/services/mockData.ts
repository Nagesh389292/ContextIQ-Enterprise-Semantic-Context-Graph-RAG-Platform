// Isolated Mock Data Layer for Development (DEMO MODE)
// All mocks are explicitly defined here and used as fallbacks when backend services are offline.

import {
  EntityMetrics, QualityMetrics, SystemHealth, ContextSearchResult,
  GraphNode, GraphEdge, OntologyClass, SHACLIssue, EvaluationMetrics,
  EvaluationTestCase, CopilotResponse
} from '../types/api';

export const MOCK_ENTITY_METRICS: EntityMetrics = {
  plants: 3,
  production_lines: 8,
  suppliers: 15,
  materials: 40,
  machines: 50,
  sensors: 150,
  employees: 100,
  production_orders: 500,
  maintenance_events: 200,
  quality_events: 150,
  telemetry_records: 10000,
  total_entities: 11216,
};

export const MOCK_QUALITY_METRICS: QualityMetrics = {
  completeness: 96.4,
  consistency: 94.8,
  validity: 97.2,
  uniqueness: 98.1,
  overall_score: 96.6,
  graph_coverage: 94.2,
  grounding_score: 91.7,
  retrieval_precision: 89.4,
};

export const MOCK_SYSTEM_HEALTH: SystemHealth = {
  api: 'healthy',
  postgresql: 'healthy',
  neo4j: 'healthy',
  vector_store: 'healthy',
  embedding_service: 'healthy',
  llm: 'healthy',
  last_ingestion: '2 minutes ago',
  indexed_documents: 48,
  graph_nodes: 12450,
  graph_relationships: 31820,
};

export const MOCK_SEARCH_RESULTS: ContextSearchResult[] = [
  {
    id: 'M001',
    title: 'Machine M001',
    category: 'Entity',
    subtitle: 'CNC Machine Unit • Northgate Assembly Plant (P001)',
    snippet: 'Operational CNC Machine manufactured by FANUC. Attached sensors: SN001, SN002, SN003. Supplied by Supplier S001.',
    score: 0.98,
    metadata: { status: 'operational', line: 'L001', supplier: 'S001' }
  },
  {
    id: 'PO-00102',
    title: 'Production Order PO-00102',
    category: 'Process',
    subtitle: 'Plan-to-Produce • Battery Module Batch',
    snippet: 'Active production order assigned to Line L004 (Battery Assembly). Target quantity: 1,200 units.',
    score: 0.92,
    metadata: { priority: 'high', status: 'in_progress' }
  },
  {
    id: 'DOC-014',
    title: 'Bearing Maintenance SOP',
    category: 'Document',
    subtitle: 'SOP Manual • Maintenance & Reliability',
    snippet: 'Standard Operating Procedure for inspection, lubrication, and vibration limits of bearing units B101.',
    score: 0.89,
    metadata: { pages: 12, process: 'Maintenance' }
  },
  {
    id: 'REL-M001-S001',
    title: 'M001 → SUPPLIED_BY → Supplier S001',
    category: 'Relationship',
    subtitle: 'Knowledge Graph Relationship',
    snippet: 'Machine M001 receives bearing components and spindle spare parts from Supplier S001.',
    score: 0.85,
    metadata: { contractTier: 1 }
  }
];

export const MOCK_GRAPH_DATA: { nodes: GraphNode[]; edges: GraphEdge[] } = {
  nodes: [
    { id: 'P001', label: 'Northgate Plant (P001)', type: 'Plant', properties: { location: 'Detroit, MI', capacity: 500 } },
    { id: 'L001', label: 'Assembly Line A (L001)', type: 'ProductionLine', properties: { status: 'active', capPerHour: 120 } },
    { id: 'M001', label: 'CNC Machine M001', type: 'Machine', properties: { status: 'operational', type: 'CNC' } },
    { id: 'SN001', label: 'Temp Sensor SN001', type: 'Sensor', properties: { type: 'temperature', unit: '°C', threshold: '85.0' } },
    { id: 'SN002', label: 'Vibration Sensor SN002', type: 'Sensor', properties: { type: 'vibration', unit: 'mm/s', threshold: '12.0' } },
    { id: 'S001', label: 'Precision Bearings Inc (S001)', type: 'Supplier', properties: { rating: 4.8, tier: 1 } },
    { id: 'MAT001', label: 'Bearing B101', type: 'Material', properties: { cost: 450.00, leadTime: 7 } },
    { id: 'PO001', label: 'Order PO-00102', type: 'ProductionOrder', properties: { status: 'in_progress', qty: 1200 } }
  ],
  edges: [
    { id: 'e1', source: 'L001', target: 'P001', label: 'LOCATED_AT' },
    { id: 'e2', source: 'M001', target: 'L001', label: 'ON_LINE' },
    { id: 'e3', source: 'M001', target: 'P001', label: 'INSTALLED_AT' },
    { id: 'e4', source: 'SN001', target: 'M001', label: 'ATTACHED_TO' },
    { id: 'e5', source: 'SN002', target: 'M001', label: 'ATTACHED_TO' },
    { id: 'e6', source: 'M001', target: 'S001', label: 'SUPPLIED_BY' },
    { id: 'e7', source: 'S001', target: 'MAT001', label: 'SUPPLIES' },
    { id: 'e8', source: 'PO001', target: 'L001', label: 'RUNS_ON' }
  ]
};

export const MOCK_ONTOLOGY_CLASSES: OntologyClass[] = [
  { class: 'http://enterprise-sce.org/ontology#Machine', name: 'Machine', label: 'Machine Unit', comment: 'Industrial machinery asset', superClass: 'EnterpriseAsset', datatype_properties: ['machineId', 'machineType', 'status'], object_properties: ['installedAt (Plant)', 'hasSensor (Sensor)', 'suppliedBy (Supplier)'], shacl_constraints: ['installedAt -> exactly 1 Plant', 'hasSensor -> min 1 Sensor'] },
  { class: 'http://enterprise-sce.org/ontology#Plant', name: 'Plant', label: 'Manufacturing Plant', comment: 'Plant facility', superClass: 'EnterpriseAsset', datatype_properties: ['plantId', 'name', 'location'], object_properties: ['hasLine (ProductionLine)'], shacl_constraints: ['plantId -> required string'] },
  { class: 'http://enterprise-sce.org/ontology#Supplier', name: 'Supplier', label: 'Supplier', comment: 'Third party vendor', superClass: 'EnterpriseResource', datatype_properties: ['supplierId', 'name', 'rating', 'tier'], object_properties: ['suppliesMaterial (Material)'], shacl_constraints: ['tier -> 1..3', 'rating -> 0.0..5.0'] },
  { class: 'http://enterprise-sce.org/ontology#Sensor', name: 'Sensor', label: 'IoT Sensor', comment: 'Machine sensor unit', superClass: 'EnterpriseAsset', datatype_properties: ['sensorId', 'sensorType', 'minThreshold', 'maxThreshold'], object_properties: ['attachedToMachine (Machine)'], shacl_constraints: ['status -> active | faulty | calibrating'] }
];

export const MOCK_SHACL_ISSUES: SHACLIssue[] = [
  { id: 'VAL-001', entity: 'Machine M018', entity_type: 'Machine', severity: 'Warning', message: 'Missing installedAt Plant relation', rule: 'sh:minCount 1 on :installedAt' },
  { id: 'VAL-002', entity: 'Machine M024', entity_type: 'Machine', severity: 'Critical', message: 'No active attached sensor found for asset', rule: 'sh:minCount 1 on :hasSensor' },
  { id: 'VAL-003', entity: 'Supplier S018', entity_type: 'Supplier', severity: 'Warning', message: 'Rating 5.4 exceeds maximum allowed 5.0', rule: 'sh:maxInclusive 5.0 on :supplierRating' },
  { id: 'VAL-004', entity: 'Sensor SN142', entity_type: 'Sensor', severity: 'Warning', message: 'Status unknown not in allowed enum', rule: 'sh:in (active faulty calibrating)' }
];

export const MOCK_EVALUATION_METRICS: EvaluationMetrics = {
  precision_at_5: 91.4,
  recall_at_10: 94.2,
  mrr: 89.8,
  faithfulness: 93.1,
  answer_relevance: 91.7,
  citation_coverage: 95.4,
  unsupported_claims_rate: 3.1,
};

export const MOCK_EVALUATION_TEST_CASES: EvaluationTestCase[] = [
  { id: 'TC-01', question: 'Which supplier provides bearing B101 for Machine M001?', expected_answer: 'Precision Bearings Inc (Supplier S001)', generated_answer: 'Supplier S001 (Precision Bearings Inc)', status: 'passed', score: 1.0 },
  { id: 'TC-02', question: 'What is the temperature threshold for Sensor SN001?', expected_answer: '85.0 °C', generated_answer: '85.0 °C on Machine M001', status: 'passed', score: 1.0 },
  { id: 'TC-03', question: 'List all active production lines in Northgate Plant (P001).', expected_answer: 'Assembly Line A (L001), Line B (L002), Paint Line (L003)', generated_answer: 'Line L001, L002, L003', status: 'passed', score: 0.95 },
  { id: 'TC-04', question: 'Identify potential causes for high vibration on CNC M005.', expected_answer: 'Bearing misalignment or lubrication deficiency per SOP-014.', generated_answer: 'Bearing wear or misalignment described in Maintenance Manual Section 4.', status: 'passed', score: 0.92 }
];

export const MOCK_COPILOT_RESPONSE: CopilotResponse = {
  id: 'COPILOT-QUERY-8821',
  answer: 'Machine M001 is experiencing repeated temperature excursions above its operating threshold of 85.0 °C. The enterprise knowledge graph and maintenance documents indicate that M001 uses Bearing B101 supplied by Precision Bearings Inc (S001). SOP-014 identifies spindle bearing misalignment or insufficient lubrication as the primary root cause.',
  recommendations: [
    'Schedule immediate technician inspection for Machine M001 bearing alignment.',
    'Check lubricant level and verify sensor SN001 calibration.',
    'If anomaly persists, contact Supplier S001 under Tier 1 SLA agreement.'
  ],
  evidence: {
    graph_relations: ['M001 → HAS_SENSOR → SN001', 'M001 → SUPPLIED_BY → S001', 'S001 → SUPPLIES → B101'],
    documents: [
      { title: 'CNC Maintenance Manual', section: 'Section 4: Thermal Excursions' },
      { title: 'Bearing Maintenance SOP', section: 'Section 2: Inspection Protocol' }
    ],
    structured_records: 23
  },
  trace: [
    { timestamp: '09:42:12.100', stage: 'Intent Identifier', details: 'Query classified: Technical Diagnostics / Root Cause' },
    { timestamp: '09:42:12.250', stage: 'Entity Resolver', details: 'Resolved entities: Machine M001, Sensor SN001, Supplier S001' },
    { timestamp: '09:42:12.400', stage: 'Knowledge Graph Traversal', details: 'Retrieved 8-node neighborhood subgraph (Neo4j)' },
    { timestamp: '09:42:12.600', stage: 'Vector Search', details: 'Retrieved 4 relevant document chunks (ChromaDB)' },
    { timestamp: '09:42:12.800', stage: 'Evidence Fusion', details: 'Fused 5 high-confidence evidence sources' },
    { timestamp: '09:42:13.100', stage: 'Grounding Validator', details: 'Passed citation and faithfulness check (Score: 98.2%)' }
  ],
  grounding_score: 98.2
};
