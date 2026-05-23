import json
from datetime import datetime, UTC
from typing import Dict, Any, List

class AnnexIVGenerator:
    def __init__(self, system_name: str, provider_name: str):
        self.system_name = system_name
        self.provider_name = provider_name

    def generate_json_report(self,
                             architecture_description: str,
                             data_profiling_summary: Dict[str, Any],
                             risk_assessment: List[Dict[str, Any]],
                             validation_metrics: Dict[str, Any]) -> str:
        report = {
            "document_type": "EU AI Act Annex IV Technical Documentation",
            "timestamp": datetime.now(UTC).isoformat(),
            "system_identification": {
                "name": self.system_name,
                "provider": self.provider_name,
                "version": "1.0.0"
            },
            "technical_specifications": {
                "architecture": architecture_description,
                "components": ["LLM", "Guardrail Orchestrator", "Vector DB"]
            },
            "data_governance": data_profiling_summary,
            "risk_management": risk_assessment,
            "validation_results": validation_metrics,
            "compliance_mapping": {
                "EU_AI_Act": "Annex IV / Article 11",
                "ISO_42001": "Clause 8.2 (AI System Impact Assessment)"
            }
        }
        return json.dumps(report, indent=2)

    def generate_markdown_report(self, data: Dict[str, Any]) -> str:
        # Simple MD representation
        md = f"# Technical Documentation: {self.system_name}\n\n"
        md += f"**Provider:** {self.provider_name}\n\n"
        md += "## Architecture\n" + data.get('architecture', 'N/A') + "\n\n"
        # ... more formatting
        return md
