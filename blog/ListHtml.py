#!/usr/bin/env python
#---coding=utf8---

from tornado.web import authenticated,HTTPError
from BaseHandler import BaseHandler,role



class ListHtml(BaseHandler):
    @authenticated
    def get(self):
        self.cursor.execute("SELECT * FROM htmls")
        htmls=self.cursor.fetchall()
        self.render("listhtml.html",htmls=htmls)
    @authenticated
    def post(self):
        action=self.get_argument("action","")
        if action=="new":
            content=self.get_argument("content","")
            if not content:
                raise HTTPError(404)
            self.cursor.execute("INSERT INTO htmls(content,status) VALUES(%s,%s)",(content,0))
        elif action=="edit":
            content=self.get_argument("content","")
            if not content:
                raise HTTPError(404)
            hid=int(self.get_argument("id","0"))
            if hid==0:
                raise HTTPError(404)
            status=int(self.get_argument("status","0"))
            self.cursor.execute("UPDATE htmls SET content=%s,status=%s WHERE id=%s",(content,status,hid))
        elif action=="delete":
            hid=int(self.get_argument("id","0"))
            if hid==0:
                raise HTTPError(404)
            self.cursor.execute("DELETE FROM htmls WHERE id=%s",hid)
        self.conn.commit()
        self.redirect("/list/html")

