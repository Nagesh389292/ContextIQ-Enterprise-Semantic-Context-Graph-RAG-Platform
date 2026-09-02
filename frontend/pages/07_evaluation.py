"""Evaluation page — stub (implemented in Phase 8)."""
import streamlit as st
st.set_page_config(page_title="Evaluation — ESCE", page_icon="📈", layout="wide")
st.markdown("# 📈 Evaluation Dashboard")
st.info("This page will be fully implemented in **Phase 8** (Evaluation Framework).\n\nDisplays retrieval accuracy (Precision@K, Recall, MRR), RAG grounding, faithfulness, citation coverage, and hallucination rate.")
st.markdown("### Metrics tracked:")
metrics = {
    "Retrieval": ["Precision@5", "Recall@5", "MRR (Mean Reciprocal Rank)"],
    "Generation": ["Faithfulness", "Answer Relevance", "Context Relevance"],
    "Grounding": ["Citation Coverage", "Unsupported Claim Rate"],
    "Graph": ["Entity Linking Accuracy", "Graph Query Accuracy"],
}
cols = st.columns(len(metrics))
for col, (category, items) in zip(cols, metrics.items()):
    with col:
        st.markdown(f"**{category}**")
        for item in items:
            st.markdown(f"- {item}")
