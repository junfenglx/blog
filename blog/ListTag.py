#!/usr/bin/env python
#---coding=utf8---

from tornado.web import authenticated,HTTPError
from BaseHandler import BaseHandler,role

class ListTag(BaseHandler):
    @authenticated
    def get(self):
        p=int(self.get_argument("paged","1"))
        self.cursor.execute("SELECT * FROM tags ORDER BY tag_count DESC LIMIT %s,%s",((p-1)*10,10))
        tags=self.cursor.fetchall()
        self.cursor.execute("SELECT count(*) AS c FROM tags")
        tags_count=self.cursor.fetchone()["c"]
        self.render("listtag.html",tags=tags,tags_count=tags_count,p=p)

