#!/usr/bin/env python
#!---coding=utf8---

from BaseHandler import LayoutHandler,post_status,comment_status,visibility,gravatar_url



class TagHandler(LayoutHandler):
    def get(self):
        tag_name=self.get_argument("name")
        self.cursor.execute("SELECT posts.post_id,title FROM posts,post_tag,tags WHERE tags.tag_name=%s AND posts.post_id=post_tag.post_id AND post_tag.tag_id=tags.tag_id",tag_name)
        tag_entries=self.cursor.fetchall()


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
        self.render("tag.html",tag_name=tag_name,tag_entries=tag_entries,recent_entries=self.recent_entries,recent_comments=self.recent_comments,categories=self.categories,tags=self.tags,htmls=self.htmls,pages=self.pages)

