#!/usr/bin/env python
#---coding=utf8---

from tornado.web import authenticated,HTTPError
from BaseHandler import BaseHandler,role,comment_status

class ListComment(BaseHandler):
    @authenticated
    def get(self):
        status=self.get_argument("comment_status","approved")
        p=int(self.get_argument("paged","1"))
        self.cursor.execute("SELECT * FROM comments WHERE comment_status=%s ORDER BY comment_date DESC LIMIT %s,%s",(comment_status[status],(p-1)*10,10))
        comments=self.cursor.fetchall()
        self.cursor.execute("SELECT count(*) AS c FROM comments WHERE comment_status=%s",comment_status[status])
        comment_count=self.cursor.fetchone()["c"]
        self.render("listcomment.html",comments=comments,comment_count=comment_count,comment_status=comment_status,status=status,p=p)


    @authenticated
    def post(self):
        comment_id=int(self.get_argument("comment","0"))
        if comment_id==0:
            raise HTTPError(404)
        post_id=int(self.get_argument("post","0"))
        if post_id==0:
            raise HTTPError(404)
        action=self.get_argument("action","")
        if not action:
            raise HTTPError(404)
        self.cursor.execute("UPDATE comments SET comment_status=%s WHERE comment_id=%s AND comment_post_id=%s",(comment_status[action],comment_id,post_id))
        self.conn.commit()
        self.redirect("/list/comment?comment_status=%s" % action)
