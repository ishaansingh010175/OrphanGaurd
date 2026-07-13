from kubernetes import client

from config import config
from models import OrphanResource, ResourceType


class ResourceDeleter:

    def __init__(self):
        self.core = client.CoreV1Api()

    def delete(self, resource: OrphanResource):

        if not resource.can_delete:
            print(
                f"[SKIP] {resource.namespace}/{resource.name} "
                "is not marked as deletable."
            )
            return

        if config.dry_run:
            print(
                f"[DRY RUN] Would delete "
                f"{resource.resource_type.value}: "
                f"{resource.namespace}/{resource.name}"
            )
            return

        try:

            if resource.resource_type == ResourceType.PVC:

                self.core.delete_namespaced_persistent_volume_claim(
                    name=resource.name,
                    namespace=resource.namespace,
                )

                print(
                    f"[DELETED] PVC "
                    f"{resource.namespace}/{resource.name}"
                )

            else:

                print(
                    f"[WARNING] Delete not implemented for "
                    f"{resource.resource_type.value}"
                )

        except Exception as e:
            print(
                f"[ERROR] Failed to delete "
                f"{resource.namespace}/{resource.name}"
            )
            print(e)