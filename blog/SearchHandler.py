#!/usr/bin/env python
#!---coding=utf8---

from BaseHandler import LayoutHandler,post_status,comment_status,visibility,gravatar_url



class SearchHandler(LayoutHandler):
    def get(self):
        s=self.get_argument("s",None)
        ts="%"+s+"%"
        self.cursor.execute("SELECT distinct posts.post_id,title FROM posts,post_tag,tags WHERE posts.post_id=post_tag.post_id AND post_tag.tag_id=tags.tag_id AND (posts.title like %s OR posts.content like %s OR tags.tag_name like %s)",(ts,ts,ts))
        search_entries=self.cursor.fetchall()
        self.render("search.html",s=s,search_entries=search_entries,recent_entries=self.recent_entries,recent_comments=self.recent_comments,categories=self.categories,tags=self.tags,htmls=self.htmls,pages=self.pages)
