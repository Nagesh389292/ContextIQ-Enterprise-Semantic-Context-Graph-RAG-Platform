"""
Enterprise Semantic Context Engine — Streamlit Main App
Multi-page application with sidebar navigation.
"""

import streamlit as st

# ─────────────────────────────────────────────────────────────
# Page configuration (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Enterprise Semantic Context Engine",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# Custom CSS — premium dark theme
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ──────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Main background ──────────────────────────────── */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #e2e8f0;
}

/* ── Sidebar ──────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.1);
}

/* ── Metric cards ─────────────────────────────────── */
[data-testid="metric-container"] {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 1rem;
    backdrop-filter: blur(10px);
}

/* ── Headers ──────────────────────────────────────── */
h1, h2, h3 {
    color: #f1f5f9 !important;
}

/* ── Accent colour ────────────────────────────────── */
.accent { color: #818cf8; }
.success { color: #34d399; }
.warning { color: #fbbf24; }
.danger  { color: #f87171; }

/* ── Cards ────────────────────────────────────────── */
.esce-card {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(8px);
    transition: border-color 0.2s ease;
}
.esce-card:hover {
    border-color: rgba(129, 140, 248, 0.5);
}

/* ── Status badge ─────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-ok      { background: rgba(52, 211, 153, 0.15); color: #34d399; border: 1px solid #34d399; }
.badge-warn    { background: rgba(251, 191, 36,  0.15); color: #fbbf24; border: 1px solid #fbbf24; }
.badge-danger  { background: rgba(248, 113, 113, 0.15); color: #f87171; border: 1px solid #f87171; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Sidebar branding
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:2.5rem;'>🔷</div>
        <div style='font-size:1.1rem; font-weight:700; color:#818cf8;'>
            ESCE
        </div>
        <div style='font-size:0.7rem; color:#64748b; letter-spacing:0.05em;'>
            ENTERPRISE SEMANTIC CONTEXT ENGINE
        </div>
    </div>
    <hr style='border-color:rgba(99,102,241,0.2); margin:0.5rem 0 1rem;'>
    """, unsafe_allow_html=True)

    st.markdown("**Navigate**")
    st.page_link("frontend/app.py",                   label="🏠 Home",                icon=None)
    st.page_link("frontend/pages/01_dashboard.py",    label="📊 Dashboard",           icon=None)
    st.page_link("frontend/pages/02_knowledge_explorer.py", label="🕸️ Knowledge Explorer", icon=None)
    st.page_link("frontend/pages/03_semantic_search.py",    label="🔍 Semantic Search",     icon=None)
    st.page_link("frontend/pages/04_rag_assistant.py",      label="🤖 RAG Assistant",        icon=None)
    st.page_link("frontend/pages/05_graph_query.py",        label="🔷 Graph Query",          icon=None)
    st.page_link("frontend/pages/06_data_quality.py",       label="✅ Data Quality",         icon=None)
    st.page_link("frontend/pages/07_evaluation.py",         label="📈 Evaluation",           icon=None)

    st.markdown("<hr style='border-color:rgba(99,102,241,0.2);'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.7rem; color:#475569;'>v1.0.0 · Manufacturing Domain</div>",
                unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Home page content
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 3rem 0 2rem;'>
    <h1 style='font-size:2.8rem; font-weight:700; background:linear-gradient(135deg,#818cf8,#38bdf8);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:0.5rem;'>
        Enterprise Semantic Context Engine
    </h1>
    <p style='font-size:1.1rem; color:#94a3b8; max-width:680px;'>
        An enterprise AI context engine combining <strong style='color:#818cf8;'>ontology-driven semantic modeling</strong>,
        <strong style='color:#38bdf8;'>knowledge graphs</strong>, 
        <strong style='color:#34d399;'>vector search</strong>, and 
        <strong style='color:#fbbf24;'>LLM-based RAG</strong> to provide grounded answers 
        over structured manufacturing data, business processes, and unstructured documents.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Feature cards ────────────────────────────────────────────
cols = st.columns(3)
features = [
    ("🧠", "Ontology Layer", "RDF/OWL/SHACL semantic schema with 28 entity classes modeling manufacturing assets, processes, and relationships.", "#818cf8"),
    ("🕸️", "Knowledge Graph", "Neo4j graph with 50+ machines, suppliers, production lines, and 12,000+ entities connected by semantic relationships.", "#38bdf8"),
    ("🤖", "Hybrid RAG", "Graph traversal + vector search fusion with grounded LLM answers, source citations, and hallucination detection.", "#34d399"),
    ("⚙️", "Agentic AI", "LangChain orchestrator that routes to SQL, graph, or vector tools based on query type.", "#fbbf24"),
    ("📋", "SPARQL + Cypher", "Dual graph query support: SPARQL over RDF store and Cypher over Neo4j for comprehensive semantic querying.", "#f472b6"),
    ("📊", "Evaluation", "Precision@K, Recall, MRR, faithfulness scoring, citation coverage, and unsupported-claim detection.", "#fb923c"),
]

for i, (icon, title, desc, color) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class='esce-card'>
            <div style='font-size:2rem; margin-bottom:0.5rem;'>{icon}</div>
            <div style='font-weight:600; color:{color}; margin-bottom:0.5rem;'>{title}</div>
            <div style='font-size:0.85rem; color:#94a3b8; line-height:1.6;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Tech stack ───────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🛠️ Technology Stack")
tech_cols = st.columns(5)
stack = [
    ("Semantic Web", ["RDFLib", "OWL", "SHACL", "SPARQL"]),
    ("Graph DB", ["Neo4j", "Cypher", "APOC"]),
    ("RAG Pipeline", ["LangChain", "ChromaDB", "Sentence-Transformers"]),
    ("Backend", ["FastAPI", "PostgreSQL", "SQLAlchemy"]),
    ("LLM & UI", ["Gemini 1.5 Pro", "Streamlit", "Plotly"]),
]
for col, (category, techs) in zip(tech_cols, stack):
    with col:
        st.markdown(f"**{category}**")
        for t in techs:
            st.markdown(f"<span style='font-size:0.8rem; color:#94a3b8;'>• {t}</span>", unsafe_allow_html=True)

st.markdown("---")
st.info("👈 Use the sidebar to navigate. Start with **📊 Dashboard** to see live system stats.")
