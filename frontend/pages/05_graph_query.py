"""Graph Query page — stub (implemented in Phase 4)."""
import streamlit as st
st.set_page_config(page_title="Graph Query — ESCE", page_icon="🔷", layout="wide")
st.markdown("# 🔷 Graph Query")
st.info("This page will be fully implemented in **Phase 4** (Knowledge Graph).\n\nExecute predefined and custom Cypher queries against Neo4j and SPARQL queries against the RDF store.")
st.markdown("### Sample Cypher queries available:")
st.code("""
-- Find all machines in a plant
MATCH (m:Machine)-[:LOCATED_AT]->(p:Plant)
WHERE p.name = 'Plant 001'
RETURN m.name, m.machine_type, m.status;

-- Trace supplier → material → production chain  
MATCH (s:Supplier)-[:SUPPLIES]->(mat:Material)<-[:USES]-(o:ProductionOrder)
RETURN s.name, mat.name, o.order_id;

-- Find machines affected by failures
MATCH (f:FailureEvent)-[:AFFECTED]->(m:Machine)
RETURN m.name, f.failure_type, f.timestamp
ORDER BY f.timestamp DESC LIMIT 10;
""", language="cypher")
