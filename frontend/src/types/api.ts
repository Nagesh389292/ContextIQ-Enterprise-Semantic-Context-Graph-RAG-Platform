// ContextIQ TypeScript API Data Contracts

export interface EntityMetrics {
  plants: number;
  production_lines: number;
  suppliers: number;
  materials: number;
  machines: number;
  sensors: number;
  employees: number;
  production_orders: number;
  maintenance_events: number;
  quality_events: number;
  telemetry_records: number;
  total_entities: number;
}

export interface QualityMetrics {
  completeness: number;
  consistency: number;
  validity: number;
  uniqueness: number;
  overall_score: number;
  graph_coverage: number;
  grounding_score: number;
  retrieval_precision: number;
}

export interface SystemHealth {
  api: 'healthy' | 'unhealthy' | 'degraded';
  postgresql: 'healthy' | 'unhealthy' | 'degraded';
  neo4j: 'healthy' | 'unhealthy' | 'degraded';
  vector_store: 'healthy' | 'unhealthy' | 'degraded';
  embedding_service: 'healthy' | 'unhealthy' | 'degraded';
  llm: 'healthy' | 'unhealthy' | 'degraded';
  last_ingestion: string;
  indexed_documents: number;
  graph_nodes: number;
  graph_relationships: number;
}

export interface ContextSearchResult {
  id: string;
  title: string;
  category: 'Entity' | 'Relationship' | 'Document' | 'Process';
  subtitle: string;
  snippet: string;
  score: number;
  metadata: Record<string, any>;
}

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties: Record<string, any>;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  label: string;
  properties?: Record<string, any>;
}

export interface GraphNeighborhood {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface OntologyClass {
  class: string;
  name: string;
  label: string;
  comment: string;
  superClass?: string;
  datatype_properties?: string[];
  object_properties?: string[];
  shacl_constraints?: string[];
}

export interface SHACLIssue {
  id: string;
  entity: string;
  entity_type: string;
  severity: 'Critical' | 'Warning' | 'Info';
  message: string;
  rule: string;
}

export interface EvaluationMetrics {
  precision_at_1?: number;
  precision_at_3?: number;
  precision_at_5?: number;
  recall_at_1?: number;
  recall_at_3?: number;
  recall_at_5?: number;
  recall_at_10?: number;
  mean_reciprocal_rank?: number;
  mrr?: number;
  mean_groundedness_score?: number;
  faithfulness?: number;
  answer_relevance?: number;
  citation_coverage?: number;
  unsupported_claims_rate?: number;
  groundedness_pass_rate?: number;
  total_test_cases?: number;
}

export interface EvaluationTestCase {
  id: string;
  category?: string;
  question: string;
  expected_doc_ids?: string[];
  expected_answer?: string;
  generated_answer?: string;
  status?: 'passed' | 'failed' | 'PASS';
  difficulty?: string;
  score?: number;
}

export interface CopilotQueryRequest {
  question: string;
  filters?: Record<string, any>;
}

export interface CopilotTraceStep {
  timestamp: string;
  stage: string;
  details: string;
}

export interface CopilotEvidence {
  graph_relations: string[];
  documents: { title: string; section: string }[];
  structured_records: number;
}

export interface CopilotResponse {
  id: string;
  answer: string;
  recommendations: string[];
  evidence: CopilotEvidence;
  trace: CopilotTraceStep[];
  grounding_score: number;
}
