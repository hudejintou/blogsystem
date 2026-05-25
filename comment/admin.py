from django.contrib import admin

from blogsystem.custom_site import custom_site
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')


custom_site.register(Comment, CommentAdmin)
