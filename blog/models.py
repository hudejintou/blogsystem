import mistune
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """文章分类模型"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
            choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        """将分类拆分为两组：导航分类和普通分类，供 base.html 顶栏/底栏使用"""
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'navs': nav_categories,           # 模板中 {% for cate in navs %} 遍历
            'categories': normal_categories,  # 模板中 {% for cate in categories %} 遍历
        }


class Tag(models.Model):
    """标签模型"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
           choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):
    """文章模型"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文", help_text="正文必须为MarkDown格式")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    # ForeignKey: 多对一 —— 多篇文章属于同一个分类
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    # ManyToManyField: 多对多 —— 一篇文章可以有多个标签，一个标签下也可以有多篇文章
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    pv = models.PositiveIntegerField(default=1)   # 页面浏览量
    uv = models.PositiveIntegerField(default=1)   # 独立访客数
    content_html = models.TextField(verbose_name="正文html代码", blank=True, editable=False)
    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id']   # 按 id 降序排列，id 越大越靠前

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        """按标签获取文章列表（旧版函数视图用，类视图已用 get_queryset 替代）"""
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            # tag.post_set: 通过 ManyToMany 反向关系，获取所有关联该标签的文章
            # select_related: 一次性查出外键关联的 owner 和 category，避免 N+1 查询
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')
        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        """按分类获取文章列表（旧版函数视图用）"""
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            # category.post_set: 通过 ForeignKey 反向关系，获取该分类下所有文章
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')
        return post_list, category

    @classmethod
    def latest_posts(cls):
        """获取已发布文章的基础查询集（类视图的 queryset 属性引用此方法）"""
        return cls.objects.filter(status=cls.STATUS_NORMAL)

    @classmethod
    def hot_posts(cls):
        """按浏览量降序获取热门文章"""
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)
        super().save(*args, **kwargs)