#!/usr/bin/env python
#---coding=utf8---

from tornado.web import authenticated,HTTPError
from BaseHandler import BaseHandler,role,post_status,visibility

class ListPost(BaseHandler):
    @authenticated
    def get(self):
        p=int(self.get_argument("paged","1"))
        get_status=self.get_argument("post_status","all")
        if get_status!="all":
            self.cursor.execute("SELECT count(*) AS c FROM posts WHERE post_status=%s",post_status[get_status])
            post_count=self.cursor.fetchone()["c"]
            self.cursor.execute("SELECT post_id,posts.author_id,nickname,posts.category_id,category_name,title,publish_date,post_status,comment_status,visibility,comment_count,view_count FROM posts, authors,categories WHERE post_status=%s AND posts.author_id=authors.author_id AND posts.category_id=categories.category_id ORDER BY publish_date DESC LIMIT %s,%s",(post_status[get_status],(p-1)*10,10))
        else:
            self.cursor.execute("SELECT count(*) AS c FROM posts")
            post_count=self.cursor.fetchone()["c"]
            self.cursor.execute("SELECT post_id,posts.author_id,nickname,posts.category_id,category_name,title,publish_date,post_status,comment_status,visibility,comment_count,view_count FROM posts, authors,categories WHERE posts.author_id=authors.author_id AND posts.category_id=categories.category_id ORDER BY publish_date DESC LIMIT %s,%s",((p-1)*10,10))
        posts=self.cursor.fetchall()
        tags={}
        for a in posts:
            self.cursor.execute("SELECT tag_name FROM post_tag,tags WHERE post_tag.post_id=%s AND post_tag.tag_id=tags.tag_id",a["post_id"])
            tags[a["post_id"]]=self.cursor.fetchall()


        self.render("listpost.html",posts=posts,post_status=get_status,post_count=post_count,p=p,tags=tags)

