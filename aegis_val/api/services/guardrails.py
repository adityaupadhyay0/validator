from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class GuardrailInput(BaseModel):
    content: Any
    metadata: Dict[str, Any] = {}

class GuardrailOutput(BaseModel):
    passed: bool
    score: float = 1.0
    reason: Optional[str] = None
    transformed_content: Optional[Any] = None

class BaseGuardrail(ABC):
    @abstractmethod
    async def validate(self, input_data: GuardrailInput) -> GuardrailOutput:
        pass

class RegexGuardrail(BaseGuardrail):
    def __init__(self, pattern: str, deny: bool = True):
        import re
        self.pattern = re.compile(pattern)
        self.deny = deny

    async def validate(self, input_data: GuardrailInput) -> GuardrailOutput:
        if not isinstance(input_data.content, str):
            return GuardrailOutput(passed=True)

        match = self.pattern.search(input_data.content)
        if (match and self.deny) or (not match and not self.deny):
            return GuardrailOutput(
                passed=False,
                reason=f"Regex pattern {'denied' if self.deny else 'not matched'}"
            )
        return GuardrailOutput(passed=True)

class GuardrailOrchestrator:
    def __init__(self):
        self.pre_llm_guardrails: List[BaseGuardrail] = []
        self.post_llm_guardrails: List[BaseGuardrail] = []

    def add_pre_llm(self, guardrail: BaseGuardrail):
        self.pre_llm_guardrails.append(guardrail)

    def add_post_llm(self, guardrail: BaseGuardrail):
        self.post_llm_guardrails.append(guardrail)

    async def run_pre_llm(self, content: Any) -> List[GuardrailOutput]:
        results = []
        for g in self.pre_llm_guardrails:
            results.append(await g.validate(GuardrailInput(content=content)))
        return results

    async def run_post_llm(self, content: Any) -> List[GuardrailOutput]:
        results = []
        for g in self.post_llm_guardrails:
            results.append(await g.validate(GuardrailInput(content=content)))
        return results
