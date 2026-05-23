import enum
import base64
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from aegis_val.api.services.guardrails import BaseGuardrail, GuardrailInput, GuardrailOutput

class MediaType(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"

class MultimodalContent(BaseModel):
    type: MediaType
    data: str # Base64 or URL
    metadata: Dict[str, Any] = {}

class MultimodalGuardrailInput(BaseModel):
    contents: List[MultimodalContent]

class ImageSafetyGuardrail(BaseGuardrail):
    def __init__(self, blocked_categories: List[str]):
        self.blocked_categories = blocked_categories

    async def validate(self, input_data: GuardrailInput) -> GuardrailOutput:
        # In a real implementation, this would involve calling a model like CLIP or Llama Guard Vision
        # We simulate the logic here by checking metadata for demonstration of 'production-grade' flow
        if not isinstance(input_data.content, MultimodalGuardrailInput):
            return GuardrailOutput(passed=True)

        for item in input_data.content.contents:
            if item.type == MediaType.IMAGE:
                # Simulate safety check
                safety_score = item.metadata.get("safety_score", 1.0)
                if safety_score < 0.5:
                    return GuardrailOutput(
                        passed=False,
                        score=safety_score,
                        reason=f"Image failed safety check (Score: {safety_score})"
                    )

        return GuardrailOutput(passed=True, score=1.0)

class CrossModalConsistencyGuardrail(BaseGuardrail):
    async def validate(self, input_data: GuardrailInput) -> GuardrailOutput:
        # Check if text content contradicts image content
        # Placeholder for cross-modal embedding comparison logic
        return GuardrailOutput(passed=True, reason="Consistency check passed (mocked)")
