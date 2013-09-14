#!/usr/bin/env python
#!---coding=utf8---

from tornado.web import authenticated
from BaseHandler import BaseHandler,role
count_status = {1:'approved_count',2:'pending_count',3:'spam_count',4:'trash_count'}

class AdminHome(BaseHandler):
    @authenticated
    def get(self):
        if self.current_user["role"]==role["reader"]:
            self.redirect("/")

        count={}
        self.cursor.execute("SELECT count(*) AS c FROM posts")
        count["post_count"]=self.cursor.fetchone()["c"]
        self.cursor.execute("SELECT count(*) AS c FROM htmls")
        count["html_count"]=self.cursor.fetchone()["c"]
        self.cursor.execute("SELECT count(*) AS c FROM categories")
        count["category_count"]=self.cursor.fetchone()["c"]
        self.cursor.execute("SELECT count(*) AS c FROM tags")
        count["tag_count"]=self.cursor.fetchone()["c"]
        self.cursor.execute("SELECT count(*) AS c FROM comments")
        count["comment_count"]=self.cursor.fetchone()["c"]
        self.cursor.execute("SELECT count(*) AS c,comment_status AS status FROM comments GROUP BY comment_status")
        comments_count = self.cursor.fetchall()
        for k in count_status.keys():
            count[count_status[k]]=0
        for cc in comments_count:
            count[count_status[cc["status"]]]=cc["c"]


        self.render("adminhome.html",**count)
