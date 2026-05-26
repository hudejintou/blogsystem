from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from config.models import SideBar
from .models import Post, Tag, Category


class CommonViewMixin:
    """
    公共 Mixin：为所有类视图注入侧边栏和导航数据。
    自身不继承任何 View，必须配合 ListView/DetailView 等多重继承使用（Mixin 要放在左边）。
    """
    def get_context_data(self, **kwargs):
        # super() 沿 MRO 链向上调用，最终到达 ListView/DetailView 的 get_context_data
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        # Category.get_navs() 返回 {'navs': [...], 'categories': [...]}
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    """首页视图：分页展示所有已发布文章"""
    queryset = Post.latest_posts()       # 只查询状态=正常的文章
    paginate_by = 10                     # 每页 10 篇
    context_object_name = 'post_list'    # 模板中遍历的变量名
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    """分类视图：继承 IndexView，按分类筛选文章"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')      # 从 URL 捕获的 category_id
        category = get_object_or_404(Category, pk=category_id)
        context.update({'category': category})             # 传给模板显示分类名
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)    # 按分类过滤文章


class TagView(IndexView):
    """标签视图：继承 IndexView，按标签筛选文章"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')                 # 从 URL 捕获的 tag_id
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({'tag': tag})                       # 传给模板显示标签名
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)              # 按标签过滤文章


class PostDetailView(CommonViewMixin, DetailView):
    """文章详情视图"""
    queryset = Post.latest_posts()       # 限定只查状态=正常的文章
    template_name = 'blog/detail.html'
    context_object_name = 'post'         # 模板中通过 {{ post }} 访问文章对象
    pk_url_kwarg = 'post_id'            # 告诉 DetailView 从 URL 的 post_id 参数提取主键
