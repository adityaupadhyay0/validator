from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4

class AgentStep(BaseModel):
    step_id: UUID = Field(default_factory=uuid4)
    agent_name: str
    action: str
    tool_input: Optional[Dict[str, Any]] = None
    observation: Optional[Any] = None
    thought: Optional[str] = None

class AgentExecutionGraph(BaseModel):
    trace_id: UUID
    steps: List[AgentStep] = []

class StateMachineAuditor:
    def __init__(self):
        pass

    def detect_loop_traps(self, graph: AgentExecutionGraph) -> List[str]:
        # Simple heuristic: repeated (action, tool_input) in sequence
        violations = []
        seen = set()
        for step in graph.steps:
            state = (step.action, str(step.tool_input))
            if state in seen:
                violations.append(f"Loop detected at action: {step.action}")
            seen.add(state)
        return violations

    def validate_tool_invocations(self, graph: AgentExecutionGraph, allowed_tools: List[str]) -> List[str]:
        violations = []
        for step in graph.steps:
            if step.action == "call_tool" and step.tool_input:
                tool_name = step.tool_input.get("name")
                if tool_name not in allowed_tools:
                    violations.append(f"Unauthorized tool invocation: {tool_name}")
        return violations
