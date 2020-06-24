#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
from datetime import datetime
from typing import Any

from kubernetes import config, client
from kubernetes.client import CoreV1Api
from kubernetes.client import ApiClient


from settings import KUBE_CONFIG

"""
id
batch
cluster
node
namespace
pod
container
cpu_request
cpu_limit
cpu_used
mem_request
mem_limit
mem_used

"""

_client = None


class ContainerResource(object):
    def __init__(self, cluster="", node=None, namespace="", pod="", container="",
                 cpu_request="", cpu_limit="", cpu_used="",
                 mem_request="", mem_limit="", mem_used="",
                 sample_time=""):
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
            "cpu_request": self.cpu_request,
            "cpu_limit": self.cpu_limit,
            "cpu_used": self.cpu_used,
            "mem_request": self.mem_request,
            "mem_limit": self.mem_limit,
            "mem_used": self.mem_used,
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


def main():
    config.load_kube_config(KUBE_CONFIG)

    cli = client.CoreV1Api()
    # nodes = cli.list_node()
    # ips = [i.metadata.name for i in nodes.items]
    # for i in ips:
    #     print(i)

    pods = cli.list_pod_for_all_namespaces(limit=1)
    print(pods)
    # pod_status = cli.read_namespaced_pod_status(namespace="ingress-nginx", name="default-http-backend-67cf578fc4-7ddj7", pretty=True)
    # print(pod_status)


    # api = client.CustomObjectsApi()
    # # metric = api.get_namespaced_custom_object(
    # #     "metrics.k8s.io", "v1beta1", "ingress-nginx", "pods",
    # #     "default-http-backend-67cf578fc4-7ddj7k"
    # # )
    # metric = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")
    #
    # js = json.dumps(metric)

    # print(js)
    # print(metric)


    pass


if __name__ == "__main__":
    main_fun()
    # main()
    pass
