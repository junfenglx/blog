#!/usr/bin/env python
#!---coding=utf8---

from BaseHandler import BaseHandler

class LogoutHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.clear_all_cookies()
        self.redirect("/")
