import pytest
from aegis_val.api.services.multimodal import ImageSafetyGuardrail, MultimodalGuardrailInput, MultimodalContent, MediaType
from aegis_val.api.services.guardrails import GuardrailInput

@pytest.mark.asyncio
async def test_image_safety_guardrail():
    g = ImageSafetyGuardrail(blocked_categories=["violence"])

    # Safe image
    safe_content = MultimodalGuardrailInput(contents=[
        MultimodalContent(type=MediaType.IMAGE, data="base64...", metadata={"safety_score": 0.9})
    ])
    res = await g.validate(GuardrailInput(content=safe_content))
    assert res.passed is True

    # Unsafe image
    unsafe_content = MultimodalGuardrailInput(contents=[
        MultimodalContent(type=MediaType.IMAGE, data="base64...", metadata={"safety_score": 0.1})
    ])
    res = await g.validate(GuardrailInput(content=unsafe_content))
    assert res.passed is False
    assert "safety check" in res.reason
