#!/usr/bin/env python
#---coding=utf8---
from HomeHandler import HomeHandler
from LoginHandler import LoginHandler
from LogoutHandler import LogoutHandler
from ArchivesHandler import ArchivesHandler
from CategoryHandler import CategoryHandler
from TagHandler import TagHandler
from PageHandler import PageHandler
from SearchHandler import SearchHandler
from AdminHome import AdminHome
from ListPost import ListPost
from EditPost import EditPost
from ListComment import ListComment
from ListTag import ListTag
from ListCategory import ListCategory
from ListHtml import ListHtml

handlers = [
    (r"/", HomeHandler),
    (r"/login", LoginHandler),
    (r"/logout",LogoutHandler),
    (r"/archives/([\d]*)",ArchivesHandler),
    (r"/category",CategoryHandler),
    (r"/tag",TagHandler),
    (r"/page",PageHandler),
    (r"/search",SearchHandler),
    (r"/admin/",AdminHome),
    (r"/list/post",ListPost),
    (r"/edit/post",EditPost),
    (r"/list/comment",ListComment),
    (r"/list/tag",ListTag),
    (r"/list/category",ListCategory),
    (r"/list/html",ListHtml),
    ]
