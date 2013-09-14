#!/usr/bin/env python
#!---coding=utf8---
from tornado.web import HTTPError
import datetime

from BaseHandler import LayoutHandler,post_status,comment_status,visibility,gravatar_url


class ArchivesHandler(LayoutHandler):
    def get(self,post_id):
        if post_id=='':
            self.write("None")
            self.finish()


        parent=int(self.get_argument("replyto","0"))
        self.cursor.execute("SELECT posts.post_id,posts.author_id,nickname,title,content,publish_date,post_status,comment_status,visibility,comment_count,view_count,tags.tag_id,tags.tag_name,categories.category_id,categories.category_name FROM posts,tags,post_tag,categories,authors WHERE posts.post_id=%s AND posts.post_id=post_tag.post_id AND post_tag.tag_id=tags.tag_id AND categories.category_id=posts.category_id AND authors.author_id=posts.author_id",post_id)
        entry=self.cursor.fetchone()
        if not entry:
            raise HTTPError(404)

        self.cursor.execute("SELECT post_id,title FROM posts WHERE post_id<%s ORDER BY post_id  DESC LIMIT 1",post_id)
        previous=self.cursor.fetchone()

        self.cursor.execute("SELECT post_id,title FROM posts WHERE post_id>%s ORDER BY post_id ASC LIMIT 1",post_id)
        next=self.cursor.fetchone()

        self.cursor.execute("SELECT comment_id,author_id,comment_author,comment_author_email,comment_author_url,comment_author_ip,comment_date,comment_content,comment_agent,comment_parent FROM comments WHERE comment_post_id=%s AND comment_status=%s",(post_id,comment_status["approved"]))
        entry_comments=self.cursor.fetchall()


        '''
        sql="SELECT post_id,title FROM posts ORDER BY publish_date DESC LIMIT 10"
        self.cursor.execute(sql)
        recent_entries=self.cursor.fetchall()

        sql="SELECT post_id,title,comment_id,comment_author FROM posts,comments WHERE posts.post_id=comments.comment_post_id ORDER BY comment_date DESC LIMIT 0,10"
        self.cursor.execute(sql)
        recent_comments=self.cursor.fetchall()

        sql="SELECT category_id,category_name FROM categories"
        self.cursor.execute(sql)
        categories=self.cursor.fetchall()

        sql="SELECT * FROM tags"
        self.cursor.execute(sql)
        tags=self.cursor.fetchall()

        htmls=[]
        '''

        self.render("archives.html",entry=entry,previous=previous,next=next,entry_comments=entry_comments,gravatar_url=gravatar_url,recent_entries=self.recent_entries,recent_comments=self.recent_comments,categories=self.categories,tags=self.tags,htmls=self.htmls,pages=self.pages,parent=parent)
    def post(self,post_id):
        date=datetime.datetime.now()
        gmt=datetime.datetime.utcnow()
        content=self.get_argument("comment",None)
        if not content:
            self.write("Bad request.")
            self.finish()
        parent=self.get_argument("comment_parent",None)
        if not parent:
            self.write("Bad request.")
            self.finish()

        user=self.get_current_user()
        if user:
            author_id=user["author_id"]
            name=user["login_name"]
            email=user["email"]
            url=user["url"]
            status=comment_status["approved"]
        else:
            author_id=0
            name=self.get_argument("author",None)
            email=self.get_argument("email",None)
            url=self.get_argument("url",None)
            if not name or not email:
                self.write("Bad request.")
                self.finish()

            self.cursor.execute("SELECT comment_id FROM comments WHERE comment_author_email=%s AND comment_status=%s",(email,comment_status["approved"]))
            if self.cursor.fetchone():
                status=comment_status["approved"]
            else:
                status=comment_status["pending"]

        agent=self.request.headers.get("User-Agent")
        if not agent:
            self.write("Bad request.")
            self.finish()

        ip=self.request.remote_ip

        if self.cursor.execute("INSERT INTO comments(comment_post_id, author_id, comment_author, comment_author_email, comment_author_url, comment_author_ip, comment_date, comment_gmt, comment_content, comment_status, comment_agent, comment_parent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(post_id,author_id,name,email,url,ip,date,gmt,content,status,agent,parent))==1:
            self.cursor.execute("UPDATE posts SET comment_count=comment_count+1 WHERE post_id = %s",post_id)

        self.conn.commit()
        self.redirect("/archives/"+post_id)
