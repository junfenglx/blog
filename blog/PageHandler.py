#!/usr/bin/env python
#!---coding=utf8---

from BaseHandler import LayoutHandler,post_status,comment_status,visibility,gravatar_url



class PageHandler(LayoutHandler):
    def get(self):
        page_name=self.get_argument("name")
        self.cursor.execute("SELECT post_id,title,content,comment_count FROM posts,categories WHERE posts.title=%s AND categories.category_name=%s AND posts.category_id=categories.category_id",(page_name,'页面'))
        page_entry=self.cursor.fetchone()

        self.cursor.execute("SELECT comment_id,author_id,comment_author,comment_author_email,comment_author_url,comment_author_ip,comment_date,comment_content,comment_agent,comment_parent FROM comments WHERE comment_post_id=%s AND comment_status=%s",(page_entry["post_id"],comment_status["approved"]))
        page_comments=self.cursor.fetchall()
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
        self.render("page.html",page_entry=page_entry,page_comments=page_comments,recent_entries=self.recent_entries,recent_comments=self.recent_comments,categories=self.categories,tags=self.tags,htmls=self.htmls,pages=self.pages,gravatar_url=gravatar_url)

