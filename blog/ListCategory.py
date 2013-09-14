#!/usr/bin/env python
#---coding=utf8---

from tornado.web import authenticated,HTTPError
from BaseHandler import BaseHandler,role


class ListCategory(BaseHandler):
    @authenticated
    def get(self):
        self.cursor.execute("SELECT * FROM categories")
        categories=self.cursor.fetchall()
        self.render("listcategory.html",categories=categories)

    @authenticated
    def post(self):
        if self.get_argument("action","")=="new":
            name=self.get_argument("category","")
            if not name:
                raise HTTPError(404)
            self.cursor.execute("SELECT category_id FROM categories WHERE category_name=%s",name)
            if self.cursor.fetchone():
                raise HTTPError(404)
            self.cursor.execute("INSERT INTO categories(category_name,category_count) VALUES(%s,%s)",(name,0))
            self.conn.commit()
            self.redirect("/list/category")
        else:
            self.write("To Do")
