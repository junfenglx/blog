#!/usr/bin/env python
#---coding=utf8---
from datetime import datetime
from tornado.web import authenticated,HTTPError
from BaseHandler import BaseHandler,role,post_status,visibility

class EditPost(BaseHandler):
    @authenticated
    def get(self):
        post_id=int(self.get_argument("post","0"))
        if post_id < 0:
            raise HTTPError(404)
        self.cursor.execute("SELECT category_id,category_name FROM categories")
        categories=self.cursor.fetchall()
        if post_id == 0:
            category_id=0
            tags=[]
            status_id=1
            visibility_id=1
            passwd=''
            comment_status=True
            title=''
            content=''
        else:
            self.cursor.execute("SELECT author_id,title,content,category_id,post_status,comment_status,visibility,post_password FROM posts WHERE post_id=%s",post_id)
            post=self.cursor.fetchone()
            if not post:
                raise HTTPError(404)
            title=post["title"]
            content=post["content"]
            category_id=post["category_id"]
            status_id=post["post_status"]
            visibility_id=post["visibility"]
            passwd=post["post_password"]
            comment_status=post["comment_status"]
            self.cursor.execute("SELECT tag_name FROM post_tag,tags WHERE post_tag.post_id=%s AND post_tag.tag_id=tags.tag_id",post_id)
            ts=self.cursor.fetchall()
            tags=[]
            for t in ts:
                tags.append(t["tag_name"])


        self.render("editpost.html",post_id=post_id,title=title,content=content,categories=categories,tags=tags,category_id=category_id,post_status=post_status,status_id=status_id,visibility=visibility,visibility_id=visibility_id,passwd=passwd,comment_status=comment_status)
    @authenticated
    def post(self):
        post_id=int(self.get_argument("post_id"))
        title=self.get_argument("title","")
        content=self.get_argument("content","")
        if not content:
            raise HTTPError(404)
        category_id=int(self.get_argument("category","0"))
        if self.cursor.execute("SELECT category_id FROM categories WHERE category_id=%s",category_id)!=1:
            raise HTTPError(404)
        tags=self.get_argument("tags","").split(",")
        status_id=int(self.get_argument("post_status","1"))
        visibility_id=int(self.get_argument("visibility","1"))
        password=self.get_argument("password","")
        if password and visibility_id!=visibility["protected"]:
            raise HTTPError(404)
        comment_status=int(self.get_argument("comment_status","1"))
        if post_id==0:
            if self.cursor.execute("INSERT INTO posts( author_id, category_id, title, content, publish_date, publish_gmt, update_date, update_gmt, post_status, comment_status, visibility, comment_count, post_password, view_count) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.current_user["author_id"],category_id,title,content,datetime.now(),datetime.utcnow(),datetime.now(),datetime.utcnow(),status_id,comment_status,visibility_id,0,password,0))!=1:
                raise HTTPError(404)
            self.cursor.execute("UPDATE categories SET category_count=category_count+1 WHERE category_id=%s",category_id)
            self.cursor.execute("SELECT post_id FROM posts WHERE title=%s",title)
            post_id=self.cursor.fetchone()["post_id"]
        elif post_id>0:
            if self.cursor.execute("UPDATE posts SET category_id=%s,title=%s,content=%s,update_date=%s,update_gmt=%s,post_status=%s,comment_status=%s,visibility=%s,post_password=%s WHERE post_id=%s AND author_id=%s",(category_id,title,content,datetime.now(),datetime.utcnow(),status_id,comment_status,visibility_id,password,post_id,self.current_user["author_id"]))!=1:
                raise HTTPError(404)
        self.update_tag(post_id,tags)
        self.conn.commit()
        self.redirect("/edit/post?post=%d" % post_id)

    def update_tag(self,post_id,tags):
        self.cursor.execute("SELECT tags.tag_id,tags.tag_name,tags.tag_count FROM post_tag,tags WHERE post_tag.post_id=%s AND post_tag.tag_id=tags.tag_id",post_id)
        stags=self.cursor.fetchall()
        for st in stags:
            if st["tag_name"] not in tags:
                self.cursor.execute("DELETE FROM post_tag WHERE post_id=%s AND tag_id=%s",(post_id,st["tag_id"]))
                if st["tag_count"]<=1:
                    self.cursor.execute("DELETE FROM tags WHERE tag_id=%s",st["tag_id"])
                else:
                    self.cursor.execute("UPDATE tags SET tag_count=tag_count-1 WHERE tag_id=%s",st["tag_id"])
            else:
                tags.remove(st["tag_name"])
        for t in tags:
            if self.cursor.execute("SELECT tag_id FROM tags WHERE tags.tag_name=%s",t)!=1:
                self.cursor.execute("INSERT INTO tags(tag_name,tag_count) VALUES(%s,%s)",(t,1))
                self.cursor.execute("SELECT tag_id FROM tags WHERE tags.tag_name=%s",t)
                tag_id=self.cursor.fetchone()["tag_id"]
                self.cursor.execute("INSERT INTO post_tag(post_id,tag_id) VALUES(%s,%s)",(post_id,tag_id))
            else:
                tag_id=self.cursor.fetchone()["tag_id"]
                if self.cursor.execute("SELECT * FROM post_tag WHERE post_id=%s AND tag_id=%s",(post_id,tag_id))!=1:
                    self.cursor.execute("INSERT INTO post_tag(post_id,tag_id) VALUES(%s,%s)",(post_id,tag_id))
                    self.cursor.execute("UPDATE tags SET tag_count=tag_count+1 WHERE tag_id=%s",tag_id)


