#encoding=utf-8
import db_utils
#init db before views
db_utils.init_db(db_utils.db_info_test)

import tornado.web
import tornado.ioloop
import router
import tornado.autoreload
from views import *
import tornado.httpserver

application = tornado.web.Application(router.route.get_routes())

if __name__ == '__main__':
    # start tornado server
    server = tornado.httpserver.HTTPServer(application)
    server.listen(8888)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()
