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
        db.execute('UPDATE auth set username="%s", mac="%s", auth_time=auth_time-1 WHERE number="%s"' % (username, mac, number))

    @classmethod
    def get_version(cls, db, app, version):
        return db.get("SELECT * FROM app where name=%s" % app)


    @classmethod
    def auth(cls, db,number,mac,username):
        result = db.get("SELECT * FROM auth where number=%s" % number)
        #验证部分
        print result
        
        if result and result['auth_time'] > 0 and (not result['username'] or result['username'] == username):
            return True
        return False


class Manage(object):
    @classmethod
    def authorization(cls, db,number,mac,username):
        if Info.auth(db,number,mac,username):
            #加密部分

            Info.set_auth_status(db,number,mac,username)
            return '加密密文'
        else:
            return '授权失败'

    @classmethod
    def updated(cls,db,app,version):
        version = Info.get_version(db,app)
        #如果版本高
        if version:
            return ['app','version','log','download']
        else:
            return '已经是最新版本'

class Auth(object):
    @classmethod
    def authenticate(cls, db, username, password):
        hashPassword = db.get('SELECT password FROM admin \
                WHERE username = %s', username)['password']
        return hashlib.md5(password).hexdigest() == hashPassword


