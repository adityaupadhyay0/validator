import pytest
from aegis_val.api.services.autonomous import PolicyEvolver
from aegis_val.api.models.base import Critique, AssessmentStatus

@pytest.mark.asyncio
async def test_policy_evolution_prompt_generation():
    evolver = PolicyEvolver()
    current_policy = "Be helpful and polite."

    critiques = [
        Critique(assessment=AssessmentStatus.FAIL, critique_text="Assistant was too brief and missed key context."),
        Critique(assessment=AssessmentStatus.PASS, critique_text="Good job.")
    ]

    prompt = await evolver.generate_evolution_prompt(current_policy, critiques)

    assert "Assistant was too brief" in prompt
    assert "Be helpful and polite." in prompt
    assert "Good job." not in prompt # Should only focus on failures
