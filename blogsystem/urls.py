from django.contrib import admin
from django.urls import path, re_path

from blog.views import (
    IndexView, CategoryView, TagView,
    PostDetailView, SearchView, AuthorView,
)
from config.views import links, LinkListView
from comment.views import CommentView
from blogsystem.custom_site import custom_site

urlpatterns = [
    # re_path: 使用正则匹配 URL；path: 使用简单路径匹配（不支持正则）
    # (?P<name>...) 是命名捕获组，捕获的值会作为关键字参数传入视图
    # as_view() 将类视图转换为 Django 可调用的视图函数
    # name 参数：在模板中通过 {% url 'name' %} 反向解析 URL，避免硬编码
    re_path(r'links/$', LinkListView.as_view(), name='links'),
    re_path(r'author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    re_path(r'search/$', SearchView.as_view(), name='search'),
    re_path(r'comment/$', CommentView.as_view(), name='comment'),
    re_path(r'^$', IndexView.as_view(), name='index'),
    re_path(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    re_path(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    re_path(r'^post/(?P<post_id>\d+)\.html$', PostDetailView.as_view(), name='post-detail'),
    re_path(r'^links/$', links, name='links'),
    # admin.site.urls 和 custom_site.urls 返回的是一组 URL 模式，不能用 name 命名
    path('super_admin/', admin.site.urls),
    path('admin/', custom_site.urls),
]
