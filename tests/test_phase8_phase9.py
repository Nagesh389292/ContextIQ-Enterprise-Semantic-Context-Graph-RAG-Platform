"""
ContextIQ — Test Suite for Phase 8 Governance & Phase 9 Agentic Copilot
Validates SHACL governance reports, data lineage, agent tool registry, and ReAct agent routing.
"""

import pytest
from governance.service import get_governance_service
from agent.tools import get_agent_tool_registry
from agent.router import get_agent_router


class TestPhase8Governance:
    """Test suite for Phase 8 Data Quality & SHACL Governance."""

    def test_shacl_report_structure(self):
        service = get_governance_service()
        report = service.get_shacl_report()
        assert "compliance_score" in report
        assert "violations_count" in report
        assert isinstance(report["issues"], list)

    def test_quality_metrics_structure(self):
        service = get_governance_service()
        metrics = service.get_quality_metrics()
        assert metrics["completeness"] > 0
        assert metrics["consistency"] > 0
        assert metrics["validity"] > 0
        assert metrics["uniqueness"] > 0

    def test_data_lineage_layers(self):
        service = get_governance_service()
        lineage = service.get_data_lineage()
        assert "layers" in lineage
        assert len(lineage["layers"]) == 5
        assert "lineage_edges" in lineage


class TestPhase9AgenticCopilot:
    """Test suite for Phase 9 ReAct Agent Copilot & Tool Registry."""

    def test_sql_guardrails(self):
        tools = get_agent_tool_registry()

        # Destructive query should be rejected
        res = tools.sql_query_tool("DROP TABLE plants;")
        assert res["status"] == "error"
        assert "Security Guardrail" in res["message"]

        # SELECT query should execute
        res_ok = tools.sql_query_tool("SELECT * FROM plants LIMIT 1;")
        assert res_ok["status"] == "success"

    def test_cypher_guardrails(self):
        tools = get_agent_tool_registry()

        # Destructive Cypher query should be rejected
        res = tools.cypher_graph_tool("MATCH (n) DELETE n")
        assert res["status"] == "error"
        assert "Security Guardrail" in res["message"]

    def test_vector_and_ontology_tools(self):
        tools = get_agent_tool_registry()

        # Vector search tool
        vec_res = tools.vector_search_tool(query="machine maintenance", top_k=2)
        assert vec_res["status"] == "success"

        # Ontology lookup tool
        onto_res = tools.ontology_lookup_tool(concept="Machine")
        assert onto_res["status"] == "success"

    def test_react_agent_router_execution(self):
        router = get_agent_router()
        res = router.run_agent(question="What maintenance applies to machine M001?")

        assert "answer" in res
        assert "execution_trace" in res
        assert len(res["execution_trace"]) >= 4
        assert res["agent_mode"] == "ReAct Tool Routing"
