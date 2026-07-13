from ai import AIAnalyzer

from models import OrphanResource
from models import ResourceType

resource = OrphanResource(
    resource_type=ResourceType.PVC,
    namespace="payments",
    name="payment-db-data",
    age_days=42,
    reason="PVC is not mounted by any running pod."
)

ai = AIAnalyzer()

result = ai.analyze(resource)

print(result.risk)
print(result.recommendation)
print(result.ai_reason)