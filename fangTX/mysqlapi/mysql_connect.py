#!/usr/bin/env python
# coding=utf-8

import MySQLdb
import ConfigParser


class MySQLConnect(object):
    config = ConfigParser.ConfigParser()
    config.read('./fangTX/mysqlapi/sql_cfg.ini')
    host = config.get('sql_cfg', 'host')
    user = config.get('sql_cfg', 'user')
    passwd = config.get('sql_cfg', 'passwd')
    dbname = config.get('sql_cfg', 'db')
    charset = config.get('sql_cfg', 'charset')
    db = MySQLdb.connect(
        host=host,
        user=user,
        passwd=passwd,
        db=dbname,
        charset=charset,
    )
    cursor = db.cursor()

    def insert_value(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print "Some thing is Wrong: %s" % e

    def close_db(self):
        self.db.close()
