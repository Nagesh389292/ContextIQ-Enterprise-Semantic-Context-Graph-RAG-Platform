"""Knowledge Explorer page — stub (implemented in Phase 4)."""
import streamlit as st
st.set_page_config(page_title="Knowledge Explorer — ESCE", page_icon="🕸️", layout="wide")
st.markdown("# 🕸️ Knowledge Explorer")
st.info("This page will be fully implemented in **Phase 4** (Neo4j Knowledge Graph).\n\nIt will allow you to search any entity and visualize its subgraph — plants, machines, sensors, suppliers, and relationships.")
st.markdown("### Preview: What you'll be able to do")
st.code("""
# Search: Machine M001
# Visualize:
#   Plant-001
#     └── Assembly Line A
#           └── Machine M001
#                 ├── Sensor S101 (Temperature)
#                 ├── Sensor S102 (Vibration)
#                 ├── Bearing B101 → Supplier S01
#                 └── Maintenance Events (3)
""")
