from openai import OpenAI

from config import config
from models import OrphanResource, RiskLevel


class AIAnalyzer:

    def __init__(self):
        self.client = OpenAI(
            api_key=config.openai_api_key
        )

    def analyze(self, resource: OrphanResource) -> OrphanResource:

        prompt = f"""
You are an experienced Kubernetes Site Reliability Engineer.

Analyze the following Kubernetes resource.

Resource Type:
{resource.resource_type.value}

Namespace:
{resource.namespace}

Name:
{resource.name}

Age:
{resource.age_days} days

Reason Detected:
{resource.reason}

Current Owner:
{resource.owner}

Currently Used By:
{resource.used_by}

Return ONLY the following format.

Risk: LOW | MEDIUM | HIGH

Recommendation:
<one sentence>

Reason:
<short explanation>
"""

        response = self.client.responses.create(
            model=config.openai_model,
            input=prompt,
        )

        output = response.output_text.strip()

        risk = RiskLevel.UNKNOWN
        recommendation = ""
        explanation = ""

        lines = output.splitlines()

        section = None

        for line in lines:

            line = line.strip()

            if line.startswith("Risk:"):
                value = line.replace("Risk:", "").strip().upper()

                if value == "LOW":
                    risk = RiskLevel.LOW
                elif value == "MEDIUM":
                    risk = RiskLevel.MEDIUM
                elif value == "HIGH":
                    risk = RiskLevel.HIGH

            elif line.startswith("Recommendation:"):
                section = "recommendation"

            elif line.startswith("Reason:"):
                section = "reason"

            elif section == "recommendation":
                recommendation += line + " "

            elif section == "reason":
                explanation += line + " "

        resource.risk = risk
        resource.recommendation = recommendation.strip()
        resource.ai_reason = explanation.strip()

        return resource