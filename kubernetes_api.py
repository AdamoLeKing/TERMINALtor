from kubernetes import client, config
import json
import time
# from kubernetes.client import configuration
# configuration.assert_hostname = False

def get_pod_ip(name: str):
    config.load_kube_config()

    api_instance = client.CoreV1Api()

    pod_ip = None
    while pod_ip is None:
        time.sleep(1)
        pod = api_instance.read_namespaced_pod(name=name, namespace="default")
        pod_ip = pod.status.pod_ip

    return pod_ip

def create_pod(name: str) -> None:
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    api_instance = client.CoreV1Api()

    try:
        pod = client.V1Pod(
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1PodSpec(
                containers=[client.V1Container(
                    name="terminaltor1",
                    image="biloucheentt26/terminaltor",
                    ports=[client.V1ContainerPort(container_port=22)]
                )]
            )
        )
    except Exception as e:
        raise e

    try:
        api_instance.create_namespaced_pod(namespace="default", body=pod)
    except Exception as e:
        raise e
    
    return get_pod_ip(name)

def delete_pod(name: str) -> None:
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    api_instance = client.CoreV1Api()

    try:
        api_instance.delete_namespaced_pod(name=name, namespace="default")
    except Exception as e:
        raise e

def get_all_pods():
    config.load_kube_config()
    api_instance = client.CoreV1Api()

    # Récupérez tous les pods dans le namespace "default"
    pods = api_instance.list_namespaced_pod(namespace="default")

    # Créez un tableau pour stocker les informations sur les pods en cours d'exécution
    running_pods = []

    # Parcourez les pods et récupérez les informations sur ceux en cours d'exécution
    for pod in pods.items:
        if pod.status.phase == "Running":
            pod_ip = pod.status.pod_ip
            if pod_ip is None:
                # Attendez que le pod soit complètement démarré et qu'une adresse IP lui soit attribuée
                time.sleep(1)
                pod = api_instance.read_namespaced_pod(name=pod.metadata.name, namespace="default")
                pod_ip = pod.status.pod_ip
            #start_time = time.strptime(pod.status.conditions[-1].last_transition_time, "%Y-%m-%dT%H:%M:%SZ")
            #up_time = time.time() - time.mktime(start_time)
            running_pods.append({
                "name": pod.metadata.name,
                "ip": pod_ip
            })

    return running_pods