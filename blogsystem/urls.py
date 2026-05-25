from django.contrib import admin
from django.urls import path, re_path

from blog.views import post_detail, post_list
from blogsystem.custom_site import custom_site
from config.views import links

urlpatterns = [
    re_path(r'^$', post_list, name='post_list'),
    re_path(r'^category/(?P<category_id>\d+)/$', post_list, name='category_list'),
    re_path(r'^tag/(?P<tag_id>\d+)/$', post_list, name='tag_list'),
    re_path(r'^post/(?P<post_id>\d+)\.html$', post_detail, name='post_detail'),
    re_path(r'^links/$', links, name='links'),
    path('super_admin/', admin.site.urls),
    path('admin/', custom_site.urls),
]
