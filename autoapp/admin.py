from django.contrib import admin
from .models import Credential, GroupLink, Post, PostSelection

admin.site.register(Credential)
admin.site.register(GroupLink)
admin.site.register(Post)
admin.site.register(PostSelection)