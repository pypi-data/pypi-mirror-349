
from probeX.framework.client.KubernetesClient import kc

class KubeService:

    def get_gpu_resources(self, namespace):
        return kc.get_gpu_usage(namespace)