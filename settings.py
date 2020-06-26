#!/usr/bin/python
# -*- coding:utf-8 -*-


# 被访问kubernetes集群配置文件路径
KUBE_CONFIG = "./config"

# 数据持久化类型，可选"csv", "mysql"
PERSISTENCE_TYPE = "csv"

# csv输出目录
CSV_DIR = "./data"

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DB = "k8s_stats"

if __name__ == "__main__":
    pass
