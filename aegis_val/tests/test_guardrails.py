import pytest
from aegis_val.api.services.guardrails import RegexGuardrail, GuardrailInput

@pytest.mark.asyncio
async def test_regex_guardrail():
    g = RegexGuardrail(pattern=r"PII-\d{4}", deny=True)

    # Test block
    res = await g.validate(GuardrailInput(content="User data: PII-1234"))
    assert res.passed is False

    # Test allow
    res = await g.validate(GuardrailInput(content="Safe content"))
    assert res.passed is True
