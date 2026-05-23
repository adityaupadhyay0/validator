# Aegis-Val Framework

Enterprise-grade AI Validation and Governance Framework.

## Architecture Summary
Aegis-Val follows a modular architecture designed for high-throughput AI validation:
- **Online Runtime Environment**: Low-latency interception of LLM traffic using a stackable guardrail orchestrator.
- **Offline Evaluation Engine**: Facilitates Critique Shadowing and LLM-as-a-Judge bootstrapping.
- **Governance & Compliance**: Automated generation of EU AI Act Annex IV documentation.
- **Autonomous Layer**: Self-healing prompt optimization and hardware-agile routing.

## Deployment
The system is designed to run on Kubernetes. See `deploy/k8s.yaml` for manifests.

## API Documentation
Once running, interactive docs are available at `/docs`.
- `POST /api/v1/critique-shadowing/submit`: Submit expert feedback.
- `POST /api/v1/critique-shadowing/compile-judge`: Bootstrap LLM judges.

## Testing
Run tests using:
```bash
python3 -m pytest aegis_val/tests/
```
