#!/usr/bin/env python
#---coding=utf8---
import tornado.web

from MySQLdb.cursors import DictCursor

post_status = dict(published=1,pending=2,draft=3,trash=4)
visibility = dict(public=1,protected=2,private=3)
comment_status=dict(approved=1,pending=2,spam=3,trash=4)
role = dict(admin=1,writer=2,reader=3)




import urllib2, hashlib

def gravatar_url(email, size=40, verify_default=False):
    """Construct the gravatar url."""
    gravatar_url = ''.join(['http://www.gravatar.com/avatar/',
    hashlib.md5(email.lower()).hexdigest(), '?s=%d' % size])
    return gravatar_url







class BaseHandler(tornado.web.RequestHandler):
    @property
    def conn(self):
        return self.application.conn
    def prepare(self):
        self.cursor=self.conn.cursor(cursorclass=DictCursor)

    def on_finish(self):
        self.cursor.close()

    def get_current_user(self):
        user_id = self.get_secure_cookie("user_id")
        if not user_id: return None
        self.cursor.execute("SELECT * FROM authors WHERE author_id = %s", int(user_id))
        user=self.cursor.fetchone()
        if not user:
            return None
        return user



class LayoutHandler(BaseHandler):
    def prepare(self):
        self.cursor=self.conn.cursor(cursorclass=DictCursor)

        sql="SELECT title,content FROM posts,categories WHERE  categories.category_name='页面' AND posts.category_id=categories.category_id"
        self.cursor.execute(sql)
        self.pages=self.cursor.fetchall()
        sql="SELECT post_id,title FROM posts WHERE posts.post_status=%d ORDER BY publish_date DESC LIMIT 10" % post_status["published"]
        self.cursor.execute(sql)
        self.recent_entries=self.cursor.fetchall()

        sql="SELECT post_id,title,comment_id,comment_author FROM posts,comments WHERE comments.comment_status=%d AND comments.comment_post_id=posts.post_id ORDER BY comment_date DESC LIMIT 0,10" % comment_status["approved"]
        self.cursor.execute(sql)
        self.recent_comments=self.cursor.fetchall()

        sql="SELECT category_id,category_name FROM categories"
        self.cursor.execute(sql)
        self.categories=self.cursor.fetchall()

        sql="SELECT * FROM tags"
        self.cursor.execute(sql)
        self.tags=self.cursor.fetchall()

        self.cursor.execute("SELECT * FROM htmls WHERE status=1")
        self.htmls=self.cursor.fetchall()
