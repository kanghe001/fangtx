#!/usr/bin/env python
# coding=utf-8

import MySQLdb


class MySQLConnect(object):
    db = MySQLdb.connect(
        host='120.24.90.29',
        user='cnfsdata1',
        passwd='cnfsdata1',
        db='cnfsdata',
        charset='utf8'
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
