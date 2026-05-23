from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aegis_val.api.core.database import get_db
from aegis_val.api.models.base import Critique, Trace, AssessmentStatus
from aegis_val.api.models.schemas import CritiqueCreate, JudgeCompileRequest
from typing import List

router = APIRouter(prefix="/critique-shadowing", tags=["Critique Shadowing"])

@router.post("/submit")
async def submit_critique(critique_in: CritiqueCreate, db: AsyncSession = Depends(get_db)):
    # Verify trace exists
    result = await db.execute(select(Trace).where(Trace.id == critique_in.trace_id))
    trace = result.scalar_one_or_none()
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found")

    new_critique = Critique(
        trace_id=critique_in.trace_id,
        expert_uid=critique_in.expert_uid,
        assessment=AssessmentStatus(critique_in.assessment),
        critique_text=critique_in.critique,
        metadata_info=critique_in.metadata
    )

    db.add(new_critique)
    await db.commit()
    await db.refresh(new_critique)

    return {"status": "success", "critique_id": str(new_critique.id)}

@router.post("/compile-judge")
async def compile_judge(request: JudgeCompileRequest, db: AsyncSession = Depends(get_db)):
    # Aggregation logic
    query = select(Critique).where(Critique.metadata_info["associated_policy_id"].astext == request.associated_policy_id).limit(request.minimum_few_shot_examples)
    result = await db.execute(query)
    critiques = result.scalars().all()

    examples = ""
    for c in critiques:
        examples += f"Expert Feedback: {c.critique_text}\nAssessment: {c.assessment}\n---\n"

    prompt = f"System Policy: {request.associated_policy_id}\n"
    prompt += f"Examples:\n{examples}\n"
    prompt += "Instructions: You are a specialized judge model. Evaluate outputs based on the provided policy and examples."

    return {
        "evaluator_name": request.evaluator_name,
        "generated_system_prompt": prompt,
        "target_model": request.target_model,
        "examples_count": len(critiques)
    }
