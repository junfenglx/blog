#!/usr/bin/env python2
#---coding=utf8---
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options


import MySQLdb


from tornado.options import define, options

from settings import settings
from handlers import handlers



define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1", help="blog database host")
define("mysql_port",default=3306,help="blog database post")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="blog", help="blog database user")
define("mysql_password", default="blog", help="blog database password")





class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.conn = MySQLdb.connect(
            host=options.mysql_host, db=options.mysql_database,
            port=options.mysql_port,charset="utf8",
            user=options.mysql_user, passwd=options.mysql_password)




def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
