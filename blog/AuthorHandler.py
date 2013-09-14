#!/usr/bin/env python
#---coding=utf8---
from BaseHandler import BaseHandler,role
from tornado.web import authenticated,HTTPError

class ListAuthor(BaseHandler):
    def get(self):

        self.cursor.execute("SELECT author_id,email,login_name,nickname,url,role,post_count FROM authors")
        authors=self.cursor.fetchall()
        self.render("listauthor.html",authors=authors)
        


class EditAuthor(BaseHandler):
    def get(self):
        pass
    def post(self):
        pass


