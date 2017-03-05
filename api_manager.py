#!/usr/bin/env python
#-*- coding:utf-8 -*-
import hashlib
import time
import os.path
import os

class Info(object):
    @classmethod
    def get_information(cls, db):
        return db.query("SELECT * FROM app ORDER BY name DESC"), db.query("SELECT * FROM auth ORDER BY time DESC")


    @classmethod
    def add_auth_status(cls, db, number, money, time):
        return db.execute('insert into auth (number, money, auth_time, time) values("%s", "%s", "%s", CURRENT_TIMESTAMP())'%(number, money, time))

    @classmethod
    def set_auth_status(cls, db, number, mac, username):
        db.execute("UPDATE auth set username=%s, mac=%s, auth_time=auth_time-1 WHERE number=%s" % (username, mac, number))

    @classmethod
    def get_version(cls, db, app, version):
        return db.query("SELECT * FROM app where name=%s" % app)


    @classmethod
    def auth(cls, db,number,mac,username):
        result = db.query("SELECT * FROM auth where number=%s" % number)
        #验证部分
        
        
        
        
        if result:
            return True
        else:
            return False


class Manage(object):
    @classmethod
    def authorization(cls, db,number,mac,username):
        if Info.auth(db,number,mac,username):
            #加密部分

            Info.set_auth_status(db,number,mac,username)
            return '加密密文'

    @classmethod
    def updated(cls,db,app,version):
        version = Info.get_version(db,app)
        #如果版本高
        if version:
            return ['app','version','log','download']
        else:
            return '已经是最新版本'


