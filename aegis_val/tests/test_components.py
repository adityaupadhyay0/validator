import pytest
from aegis_val.api.services.compliance import AnnexIVGenerator
import json

def test_annex_iv_generation():
    generator = AnnexIVGenerator(system_name="Aegis-Test", provider_name="Aegis-Corp")
    report_json = generator.generate_json_report(
        architecture_description="Test Architecture",
        data_profiling_summary={"samples": 100},
        risk_assessment=[{"risk": "bias", "mitigation": "filtering"}],
        validation_metrics={"accuracy": 0.99}
    )

    report = json.loads(report_json)
    assert report["system_identification"]["name"] == "Aegis-Test"
    assert report["technical_specifications"]["architecture"] == "Test Architecture"
    assert "Annex IV" in report["compliance_mapping"]["EU_AI_Act"]

from aegis_val.api.services.agent_auditor import StateMachineAuditor, AgentExecutionGraph, AgentStep
from uuid import uuid4

def test_agent_loop_detection():
    auditor = StateMachineAuditor()
    trace_id = uuid4()

    # Create a loop: same action and tool_input
    step1 = AgentStep(agent_name="TestBot", action="search", tool_input={"q": "test"})
    step2 = AgentStep(agent_name="TestBot", action="search", tool_input={"q": "test"})

    graph = AgentExecutionGraph(trace_id=trace_id, steps=[step1, step2])
    violations = auditor.detect_loop_traps(graph)

    assert len(violations) > 0
    assert "Loop detected" in violations[0]
