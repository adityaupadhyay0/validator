import asyncio
from typing import Any, Dict, List, Callable
from aegis_val.api.services.guardrails import GuardrailInput

class SelfCorrectionLoop:
    def __init__(self, generator_fn: Callable[[str], asyncio.Future]):
        self.generator_fn = generator_fn
        self.max_retries = 3

    async def execute(self, prompt: str, guardrails: List[Any]) -> Dict[str, Any]:
        current_prompt = prompt
        attempts = 0

        while attempts < self.max_retries:
            attempts += 1
            response = await self.generator_fn(current_prompt)

            violations = []
            for g in guardrails:
                res = await g.validate(GuardrailInput(content=response))
                if not res.passed:
                    violations.append(res.reason)

            if not violations:
                return {"content": response, "status": "passed", "attempts": attempts}

            # Construct correction prompt
            correction_instruction = f"\n\nValidation Failure: Your previous output violated the following policies: {', '.join(violations)}. Please rewrite the output to comply with these policies."
            current_prompt += correction_instruction

        return {"content": response, "status": "failed", "attempts": attempts, "violations": violations}
