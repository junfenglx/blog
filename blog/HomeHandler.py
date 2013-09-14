#!/usr/bin/env python
#!---coding=utf8---

from BaseHandler import LayoutHandler,post_status

class HomeHandler(LayoutHandler):
    def get(self):
        p=int(self.get_argument("paged",'1'))

        sql="SELECT posts.post_id,posts.author_id,nickname,title,content,publish_date,post_status,comment_status,visibility,comment_count,view_count,tags.tag_id,tags.tag_name,categories.category_id,categories.category_name FROM posts,tags,post_tag,categories,authors WHERE posts.post_status=%d AND posts.post_id=post_tag.post_id AND post_tag.tag_id=tags.tag_id AND categories.category_id=posts.category_id AND authors.author_id=posts.author_id ORDER BY posts.publish_date DESC LIMIT %d,%d" %(post_status["published"],10*(p-1),10)
        self.cursor.execute(sql)
        entries=self.cursor.fetchall()

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

        ht'ls=[]
        '''
        self.render("home.html",entries=entries,recent_entries=self.recent_entries,recent_comments=self.recent_comments,categories=self.categories,tags=self.tags,htmls=self.htmls,pages=self.pages,p=p)

