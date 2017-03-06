#!/usr/bin/env python
#-*- coding:utf-8 -*-
import hashlib
import time
import os.path
import os
import datetime

class Info(object):
    @classmethod
    def get_information(cls, db):
        app = db.query("SELECT * FROM app ORDER BY name DESC")
        auths = db.query("SELECT * FROM auth ORDER BY time DESC")
        data = {'money':db.get("SELECT sum(money) from auth")['sum(money)'],'num':db.get("select count(*) from auth")['count(*)']}
        for auth in auths:
            auth.percentage = '%s/%d' % (time.time() - time.mktime(auth.time.timetuple()),  86400*(30 if auth.money==30 else 60))
        return app, auths ,data
        
    @classmethod
    def add_auth_status(cls, db, number, money, auth_time):
        db.execute('insert into auth (number, money, auth_time, time) values("%s", %s, %s, CURRENT_TIMESTAMP())'%(number, money, auth_time))

    @classmethod
    def set_auth_status(cls, db, id, number, money, username, auth_time):
        db.execute('UPDATE auth set username="%s", money=%s, auth_time=%s, number="%s" WHERE id=%s' % (username, money, auth_time, number, id))

    @classmethod
    def get_version(cls, db, app):
        return db.get('SELECT * FROM app where name="%s"' % app)

    @classmethod
    def set_app_info(cls, db, app, version, description, download):
        db.execute('UPDATE app set version=%s, description="%s", download="%s", time=CURRENT_TIMESTAMP() WHERE name="%s"' % (version, description, download, app))
    
    @classmethod
    def add_app_info(cls, db, app, version, description, download):
        db.execute('insert into app (name, version, description, download, time) values("%s", %s, "%s", "%s", CURRENT_TIMESTAMP())'%(app, version, description, download))

    @classmethod
    def del_auth(cls, db, id):
        db.execute('DELETE FROM auth WHERE id=%s' % id)
    
    @classmethod
    def del_app(cls, db, id):
        db.execute('DELETE FROM app WHERE id=%s' % id)

    @classmethod
    def auth(cls, db,number,mac,username):
        result = db.get("SELECT * FROM auth where number=%s" % number)
        #验证部分
        
        if result and result['auth_time'] > 0 and (not result['username'] or result['username'] == username):
            Info.set_auth_status(db, result['id'], number, result['money'], username, result['auth_time']-1)
            return True
        return False


class Manage(object):
    @classmethod
    def authorization(cls, db,number,mac,username):
        if Info.auth(db,number,mac,username):
            #加密部分

            
            return '加密密文'
        else:
            return '授权失败'

    @classmethod
    def updated(cls,db,app,version):
        app = Info.get_version(db,app)

        #如果版本高
        if app and app['version'] > version:
            print '有新版本'
            return '有新版本'
        else:
            return '已经是最新版本'

class Auth(object):
    @classmethod
    def authenticate(cls, db, username, password):
        hashPassword = db.get('SELECT password FROM admin \
                WHERE username = %s', username)['password']
        return hashlib.md5(password).hexdigest() == hashPassword


