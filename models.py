from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ResourceType(str, Enum):
    PVC = "PersistentVolumeClaim"
    CONFIGMAP = "ConfigMap"
    SECRET = "Secret"
    SERVICE = "Service"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"


class OrphanResource(BaseModel):
    """
    Represents a Kubernetes resource that may be orphaned.
    """

    resource_type: ResourceType

    namespace: str

    name: str

    age_days: int = 0

    reason: str

    used_by: list[str] = Field(default_factory=list)

    owner: Optional[str] = None

    ai_reason: Optional[str] = None

    recommendation: Optional[str] = None

    risk: RiskLevel = RiskLevel.UNKNOWN

    can_delete: bool = False


class ScanResult(BaseModel):
    """
    Result of a cluster scan.
    """

    cluster_name: str = "default"

    resources: list[OrphanResource] = Field(default_factory=list)

    def add(self, resource: OrphanResource):
        self.resources.append(resource)

    @property
    def total(self) -> int:
        return len(self.resources)

    @property
    def low_risk(self) -> int:
        return len(
            [r for r in self.resources if r.risk == RiskLevel.LOW]
        )

    @property
    def medium_risk(self) -> int:
        return len(
            [r for r in self.resources if r.risk == RiskLevel.MEDIUM]
        )

    @property
    def high_risk(self) -> int:
        return len(
            [r for r in self.resources if r.risk == RiskLevel.HIGH]
        )