#!/usr/bin/env python
#-*- coding:utf-8 -*-
import torndb
import tornado.httpserver
import tornado.web
import tornado.ioloop
import os.path
import ConfigParser
import re
import sys

from manager import *
from tornado.options import define, options

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/authorization', AuthHandler),
            (r"/update", UpdateHandler),
            (r"/admin", ManageHandler),
            (r"/set_auth", SetAuthHandler),
            (r"/set_app", SetAppHandler),
            (r"/del_auth", DelAuthHandler),
            (r"/del_app", DelAppHandler),
            (r"/add_app", AddAppHandler),
            (r"/add_auth", AddAuthHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/admin_auth', AdminHandler),
            (r'.*', BaseHandler)
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            autoescape=None,
            xsrf_cookies=False,
            cookie_secret='6de683f6e8f038f62863fe27a17573e5',
            login_url='/login',
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password
        )


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write_error(404)

    def post(self):
        self.write_error(404)

    @property
    def db(self):
        return self.application.db

    def write_error(self, status_code, **kwargs):
        if status_code == 400:
            error = "400: Bad Request"
            self.render('404.html')
        if status_code == 405:
            error = "405: Method Not Allowed"
            self.render('404.html')
        if status_code == 404:
            self.render('404.html')

    def get_current_user(self):
        return self.get_secure_cookie('user')

    def isAdmin(self):
        if self.get_secure_cookie('user'):
            return True
        else:
            return False

#主页
class HomeHandler(BaseHandler):
    def get(self):
        self.render('index.html')

#授权
class AuthHandler(BaseHandler):
    def post(self):
        number = self.get_argument('number','00000000')
        mac = self.get_argument('mac','')
        username = self.get_argument('username','')
        encrypt = Manage.authorization(self.db,number,mac,username)
        self.write(encrypt)

#获取更新信息
class UpdateHandler(BaseHandler):
    def post(self):
        app = self.get_argument('name','')
        version = self.get_argument('version','')
        result = Manage.updated(self.db,app,float(version))
        self.write(result)

#添加验证条目
class AddAuthHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        number = self.get_argument('number','')
        money = self.get_argument('money','0')
        auth_time = self.get_argument('auth_time','4')
        Info.add_auth_status(self.db,number,money,auth_time)
        self.write('ok')

class SetAuthHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        id = self.get_argument('id','')
        number = self.get_argument('number','')
        money = self.get_argument('money','30')
        auth_time = self.get_argument('auth_time','4')
        username = self.get_argument('username','')
        Info.set_auth_status(self.db, id, number, money, username, auth_time)
        self.write('ok')

#设置app信息                   
class SetAppHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        app = self.get_argument('name','')
        version = self.get_argument('version','0')
        description = self.get_argument('description','')
        download = self.get_argument('download','')
        Info.set_app_info(self.db, app, version, description, download)
        
#添加app信息                   
class AddAppHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        app = self.get_argument('name','')
        version = self.get_argument('version','0')
        description = self.get_argument('description','')
        download = self.get_argument('download','')
        Info.add_app_info(self.db, app, version, description, download)


#删除auth信息                   
class DelAuthHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        id = self.get_argument('id','')
        Info.del_auth(self.db, id)

#删除auth信息                   
class DelAppHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        id = self.get_argument('id','')
        Info.del_app(self.db, id)

#后台主页
class ManageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        apps, auths, data = Info.get_information(self.db)
        self.render('admin.html',auths = auths, apps = apps, data = data)


class LoginHandler(BaseHandler):
    def get(self):
        next = self.get_argument('next', '/')
        self.render('login.html', next=next)

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect('/', permanent=True)



#管理员验证--------------------------------------------------------------------------
class AdminHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        try:
            if self.validate(username) is None:
                raise

            if Auth.authenticate(self.db, username, password):
                self.set_secure_cookie("user", "admin", expires_days=1)
                self.redirect(self.get_argument('next', '/'), permanent=True)
            else:
                error = "Authentication failure"
                self.render('404.html')
        except:
            error = "The user not exists"
            self.render('404.html')

    def validate(self, username):
        regex = re.compile(r'^[\w\d]+$')
        return regex.match(username)

#管理员验证--------------------------------------------------------------------------

def main():
    config = ConfigParser.ConfigParser()
    config.read('blog.cfg')
    mysql = dict(config.items('mysql'))
    blog = dict(config.items('blog'))

    define("port", default=int(blog['port']), type=int)
    define("mysql_host", default="127.0.0.1:3306")
    define("mysql_database", default=mysql['database'])
    define("mysql_user", default=mysql['user'])
    define("mysql_password", default=mysql['password'])
    define("user", default=blog['user'])


    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
