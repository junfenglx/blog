#!/usr/bin/env python
#!---coding=utf8---

from BaseHandler import BaseHandler
class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect("/")
        self.render('login.html')
    def post(self):
        if self.current_user:
            self.redirect("/")
        name=self.get_argument("name")
        passwd=self.get_argument("passwd")
        self.cursor.execute("SELECT * FROM authors WHERE login_name=%s",name)
        user=self.cursor.fetchone()
        if user:
            if user['login_name'] and user['password']==passwd:
                self.set_secure_cookie("user_id",str(user['author_id']))
                self.redirect("/")
        else:
            self.redirect('/login')
