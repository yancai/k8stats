#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
from datetime import datetime

from kubernetes import config, client
from kubernetes.client import CoreV1Api

from settings import KUBE_CONFIG


_client = None
_container_metrics_map = dict()


def format_cpu(cpu):
    """规整cpu单位为n
    1n = 10^-9
    1u = 10^-6
    1m = 10^-3

    :return:
    """

    if cpu is None:
        return cpu

    if cpu.endswith("n"):
        return cpu
    if cpu.endswith("m"):
        value = int(cpu[0:-1]) * 1000
        return str(value) + "n"
    if cpu.isdigit():
        value = int(cpu) * 1000 * 1000
        return str(value) + "n"


def format_mem(mem):
    """规整memory单位为Ki
    1 Mi = 1024 Ki
    1 Gi = 1024 Mi

    :return:
    """

    if mem is None:
        return mem

    if mem.endswith("Ki"):
        return mem
    if mem.endswith("Mi"):
        value = int(mem[0:-2]) * 1024
        return str(value) + "Ki"
    if mem.endswith("Gi"):
        value = int(mem[0:-2]) * 1024 * 1024
        return str(value) + "Gi"


class ContainerResource(object):
    def __init__(self,
                 cluster=None, node=None, namespace=None, pod=None,
                 container=None,
                 cpu_request=None, cpu_limit=None, cpu_used=None,
                 mem_request=None, mem_limit=None, mem_used=None,
                 sample_time=None):
        super().__init__()
        self.cluster = cluster
        self.node = node
        self.namespace = namespace
        self.pod = pod
        self.container = container
        self.cpu_request = cpu_request
        self.cpu_limit = cpu_limit
        self.cpu_used = cpu_used
        self.mem_request = mem_request
        self.mem_limit = mem_limit
        self.mem_used = mem_used
        self.sample_time = sample_time

    def to_dict(self):
        return {
            "cluster": self.cluster,
            "node": self.node,
            "namespace": self.namespace,
            "pod": self.pod,
            "container": self.container,
            "cpu_request": format_cpu(self.cpu_request),
            "cpu_limit": format_cpu(self.cpu_limit),
            "cpu_used": format_cpu(self.cpu_used),
            "mem_request": format_mem(self.mem_request),
            "mem_limit": format_mem(self.mem_limit),
            "mem_used": format_mem(self.mem_used),
            "sample_time": self.sample_time,
        }


def list_container_res_by_pod(pod_data):
    """列出某一个pod下的所有container资源使用情况
    包含cpu, mem的request, limit, used值

    :param pod_data:
    :return:
    :rtype: list
    """
    con_reses = []
    for c in pod_data.spec.containers:
        con_res = ContainerResource()
        con_res.node = pod_data.spec.node_name
        con_res.namespace = pod_data.metadata.namespace
        con_res.pod = pod_data.metadata.name
        con_res.container = c.name
        if c.resources.requests is not None:
            con_res.cpu_request = c.resources.requests.get("cpu", None)
            con_res.mem_request = c.resources.requests.get("memory", None)

        if c.resources.limits is not None:
            con_res.mem_limit = c.resources.limits.get("memory", None)
            con_res.cpu_limit = c.resources.limits.get("cpu", None)

        con_metric_map = get_container_metrics_by_namespaced(con_res.namespace)
        key = "-".join([con_res.namespace, con_res.pod, con_res.container])
        con_res.cpu_used = con_metric_map.get(key, {}).get("cpu", None)
        con_res.mem_used = con_metric_map.get(key, {}).get("memory", None)

        con_res.sample_time = con_metric_map.get(key, {}).get("timestamp", None)

        if con_res.cpu_used is not None:
            con_reses.append(con_res)

    return con_reses


def list_container_res_by_namespace(ns):
    """列出某一个命名空间下的所有container资源使用情况
    包含cpu, mem的request, limit, used值

    :return:
    """
    k8scli = get_k8s_client()
    data = k8scli.list_namespaced_pod(ns)

    container_res_list = []
    for pod in data.items:
        con_res = list_container_res_by_pod(pod)
        container_res_list.extend(con_res)

    return container_res_list


def init():
    """初始化k8s客户端配置

    :return:
    """
    config.load_kube_config(KUBE_CONFIG)


def get_k8s_client():
    """获取k8s客户端连接

    :return:
    :rtype: CoreV1Api
    """
    global _client
    if _client is None:
        _client = client.CoreV1Api()

    return _client


def get_container_metrics_by_namespaced(ns):
    """获取某一namespace下的所有容器资源已使用值
    [
      {
        "cpu": "1166876n",
        "memory": "9716Ki",
        "timestamp": "2020-06-25T03:07:06Z",
      }
    ]

    :param ns:
    :return:
    """
    global _container_metrics_map
    if ns not in _container_metrics_map:
        api = client.CustomObjectsApi()
        data = api.list_namespaced_custom_object(
            "metrics.k8s.io", "v1beta1", ns, "pods")

        cmap = dict()

        for pod in data["items"]:
            pod_name = pod["metadata"]["name"]
            for container in pod["containers"]:
                key = "-".join([ns, pod_name, container["name"]])
                cmap[key] = container["usage"]
                cmap[key]["timestamp"] = pod["timestamp"]

        _container_metrics_map[ns] = cmap

    return _container_metrics_map[ns]


def main_fun():
    init()
    k8scli = get_k8s_client()
    data = k8scli.list_namespace()
    namespaces = [i.metadata.name for i in data.items]

    con_reses = []
    for ns in namespaces:
        con_reses.extend(list_container_res_by_namespace(ns))

    result = {"data": [r.to_dict() for r in con_reses]}
    print(json.dumps(result))


if __name__ == "__main__":
    start = datetime.now()
    main_fun()
    end = datetime.now()

    print("start: {}\nend: {}\nused: {}".format(
        start, end, end - start
    ))
    pass
