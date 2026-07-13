from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException

from models import OrphanResource, ResourceType


class KubernetesScanner:
    def __init__(self):
        self._load_config()
        self.core = client.CoreV1Api()

    def _load_config(self):
        """
        Load kubeconfig if running locally,
        otherwise fall back to in-cluster config.
        """
        try:
            config.load_kube_config()
            print("✓ Loaded local kubeconfig")
        except ConfigException:
            config.load_incluster_config()
            print("✓ Loaded in-cluster config")

    def get_all_pods(self):
        return self.core.list_pod_for_all_namespaces().items

    def get_all_pvcs(self):
        return self.core.list_persistent_volume_claim_for_all_namespaces().items

    def scan_orphan_pvcs(self):
        """
        Find PVCs that are not mounted by any running pod.
        """

        pods = self.get_all_pods()
        pvcs = self.get_all_pvcs()

        mounted_pvcs = set()

        # Build list of PVCs currently mounted by Pods
        for pod in pods:
            namespace = pod.metadata.namespace

            if not pod.spec.volumes:
                continue

            for volume in pod.spec.volumes:
                if volume.persistent_volume_claim:
                    mounted_pvcs.add(
                        (
                            namespace,
                            volume.persistent_volume_claim.claim_name,
                        )
                    )

        orphan_resources = []

        # Check every PVC
        for pvc in pvcs:
            namespace = pvc.metadata.namespace
            name = pvc.metadata.name

            if (namespace, name) not in mounted_pvcs:
                orphan_resources.append(
                    OrphanResource(
                        resource_type=ResourceType.PVC,
                        namespace=namespace,
                        name=name,
                        reason="PVC is not mounted by any running Pod.",
                    )
                )

        return orphan_resources