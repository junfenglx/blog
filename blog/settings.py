#!/usr/bin/env python
#---coding=utf8---

import os.path

settings = dict(
    blog_title=u"algu.me",
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=True,
    cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    login_url="/login",
    debug=True,
    )
