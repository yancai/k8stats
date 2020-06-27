# Kubernetes 资源统计工具

本工程使用`Python`语言，实现了针对特定kubernetes集群中所有`Pod`中容器资源（CPU、内存）的统计

 - [工程目录结构说明](#工程目录结构说明)
 - [快速使用指北](#快速使用指北)
   - [环境依赖](#环境依赖)
   - [依赖包安装](#依赖包安装)
     - [方法一：使用Pipenv](#方法一使用Pipenv)
     - [方法二：使用pip](#方法二使用pip)
   - [基本配置说明](#基本配置说明)
   - [脚本使用方式](#脚本使用方式)

## 工程目录结构说明

```
├── Pipfile             # pipenv工程文件
├── Pipfile.lock        # pipenv工程文件
├── requirements.txt    # pipenv工程文件
├── ReadMe.md           # 说明文件
├── config              # 默认连接的kubernetes集群的kube-config文件
├── schema.sql          # MySQL数据库初始化脚本
├── settings.py         # 配置文件
├── stats.py            # 主程序入口，提供kubernetes资源统计功能
└── utils/              # 工具类
```

## 快速使用指北

### 环境依赖

Python 3.7+

### 依赖包安装

#### 方法一：使用Pipenv

已经具备[`Pipenv`](https://pipenv.pypa.io/)的情况下，进入工程目录，执行如下命令创建虚拟环境及安装依赖

```shell script
pipenv install

# 使用如下命令切换至已经创建好的虚拟环境
pipenv shell
```

#### 方法二：使用pip

已经具备[`pip`](https://pip.pypa.io/)的情况下，进入工程目录，执行如下命令安装依赖

```shell script
pip install -r requirements.txt
```

*不同环境的pip可能不同，也可能为`pip3`*

### 基本配置说明

`config`文件是所需连接kubernetes集群的`kube-config`文件，**请注意修改为对应集群的kube-config**

本脚本提供了两种数据持久化方式

1. 以csv文件保存单次的数据查询结果（默认方式）  
    默认存储至工程目录下的`data`文件夹中
2. 对接MySQL，将数据查询结果存储至MySQL  
    使用MySQL的话，需要提前使用`schema.sql`初始化数据库表

更详细配置参看`settings.py`，

### 脚本使用方式

使用如下命令运行`stats.py`文件，稍等片刻即可完成统计，在配置的输出方式中查看结果即可

```shell script
python stats.py
```

*不同Python环境，可能使用的Python不同，可能为`python3`, `python3.7`等*
