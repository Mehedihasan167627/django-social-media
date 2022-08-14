from django.contrib import admin

from .models import*

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Comment)
