from typing import List, Dict, Any, Optional
import jinja2
from aegis_val.api.models.base import Critique, AssessmentStatus

class PolicyEvolver:
    def __init__(self, llm_client: Optional[Any] = None):
        self.llm_client = llm_client
        self.template_env = jinja2.Environment(loader=jinja2.BaseLoader())
        self.evolution_template = self.template_env.from_string("""
Current System Policy:
{{ current_policy }}

Expert Feedback Loop Results:
{% for critique in critiques %}
- ASSESSMENT: {{ critique.assessment }}
  FEEDBACK: {{ critique.critique_text }}
{% endfor %}

TASK:
Analyze the failures above. Identify patterns of non-compliance.
Rewrite the system policy to explicitly address these failure modes while maintaining all original safety and functional requirements.
DO NOT introduce new constraints that were not implied by the feedback.
""")

    async def generate_evolution_prompt(self,
                                       current_policy: str,
                                       critiques: List[Critique]) -> str:
        # Filter for failures to focus evolution
        fail_critiques = [c for c in critiques if c.assessment == AssessmentStatus.FAIL]

        if not fail_critiques:
            return current_policy

        prompt = self.evolution_template.render(
            current_policy=current_policy,
            critiques=fail_critiques
        )
        return prompt

    async def evolve(self, current_policy: str, critiques: List[Critique]) -> str:
        prompt = await self.generate_evolution_prompt(current_policy, critiques)

        if self.llm_client:
            # response = await self.llm_client.complete(prompt)
            # return response.text
            pass

        return prompt # Fallback to returning the prompt for human/external execution
