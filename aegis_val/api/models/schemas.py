from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID

class CritiqueCreate(BaseModel):
    trace_id: UUID
    expert_uid: str
    assessment: str # PASS/FAIL
    critique: str
    metadata: Dict[str, Any] = {}

class JudgeCompileRequest(BaseModel):
    evaluator_name: str
    associated_policy_id: str
    minimum_few_shot_examples: int = 5
    target_model: str

class GuardrailResponse(BaseModel):
    guardrail_id: str
    passed: bool
    reason: Optional[str] = None

class TraceResponse(BaseModel):
    trace_id: UUID
    status: str
    results: List[GuardrailResponse]
