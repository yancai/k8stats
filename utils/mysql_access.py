#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Documentation"""

import mysql.connector


class MySQLAccess(object):
    """MySQL数据库访问类
    """

    def __init__(self, host, port, user, passwd, db, charset="utf8"):
        """

        :param host:
        :param port:
        :param user:
        :param passwd:
        :param db:
        :param charset:
        """
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._db = db
        self._charset = charset
        self._connection = mysql.connector.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            passwd=self._passwd,
            db=self._db,
            charset=self._charset
        )
        self._inited = True

    def execute(self, sql, params=None, need_fetch=True, commit=False):
        """执行sql语句并返回结果

        Example:
            access.execute(
                "SELECT * FROM uc_user WHERE name = %s AND gender = %s",
                ("test", "0")
            )

        :param string sql: sql语句
        :param tuple params: sql参数
        :return: 执行sql结果
        """

        assert self._inited, "not initialized!"
        cursor = self._connection.cursor()
        cursor.execute(sql, params, multi=True)
        if commit:
            self._connection.commit()
        result = cursor.fetchall() if need_fetch else None
        cursor.close()
        return result

    def call_proc(self, process, params, out_index):
        """执行存储过程

        Example:
            access.call_proc(
                "listStudentByName",
                ("%test%",)
            )

        :param string process: 存储过程名
        :param tuple params: 存储过程参数
        :param int out_index: 返回参数的索引
        :return: 执行存储过程结果
        """

        assert self._inited, "not initialized!"
        cursor = self._connection.cursor()
        cursor.callproc(process, params)
        cursor.execute("SELECT @_%s_%s;" % (process, out_index))
        result = cursor.fetchone()[0]
        self._connection.commit()
        return result

    def close(self):
        """关闭数据库连接
        """
        self._connection.close()


if __name__ == "__main__":
    pass
