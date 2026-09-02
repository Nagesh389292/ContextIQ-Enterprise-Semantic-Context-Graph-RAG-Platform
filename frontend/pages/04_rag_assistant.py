"""RAG Assistant page — stub (implemented in Phase 6)."""
import streamlit as st
st.set_page_config(page_title="RAG Assistant — ESCE", page_icon="🤖", layout="wide")
st.markdown("# 🤖 RAG Assistant")
st.info("This page will be fully implemented in **Phase 6** (Hybrid RAG).\n\nAsk natural language questions about your manufacturing enterprise. The assistant combines graph traversal, vector search, and Gemini LLM with source citations.")
st.markdown("### Example questions:")
for q in [
    "Why did Machine M001 experience repeated overheating?",
    "Which supplier provides bearing B101?",
    "What is the maintenance procedure for CNC machines?",
    "Which machines in Plant-001 have had failures in the last 90 days?",
    "What materials does Supplier S02 provide and which production orders use them?",
]:
    st.markdown(f"- *{q}*")
