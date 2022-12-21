from django.contrib import admin
from .models import *
# Register your models here.

class BlogAdmin(admin.AdminSite):
    site_header = 'Blog administration'
    index_title="Admin Blog"

blog_admin=BlogAdmin(name="blog-admin")

blog_admin.register(Post)
blog_admin.register(Comment)
blog_admin.register(Like)


# admin.site.register(Post)
# admin.site.register(Comment)
# admin.site.register(Like)