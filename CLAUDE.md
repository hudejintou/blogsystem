# blogsystem — Django 博客系统

## 项目结构

```
blogsystem/              # Django 项目配置（settings, urls, wsgi）
  settings/
    base.py              # 公共配置（SQLite, 中文, 上海时区, THEME 变量）
    develop.py           # 开发环境（DEBUG=True）
  themes/                # 主题目录（前端模板 + 静态文件）
    default/             # 默认主题
    bootstrap/           # Bootstrap 主题（第8章）
      templates/
        blog/            # base.html, list.html, detail.html
        config/          # links.html, blocks/
      static/
        css/bootstrap/   # Bootstrap CSS
        js/bootstrap/    # Bootstrap JS
blog/                    # 博客 APP — Post, Category, Tag 模型
comment/                 # 评论 APP
config/                  # 配置 APP — 友情链接、侧边栏
demo.html               # Bootstrap 静态演示页（浏览器直接打开）
```

## 环境配置

- **Python**: 3.14（Windows）/ 3.13（Mac），各机器独立管理 `.venv`
- **配置切换**: 通过环境变量 `BLOGSYSTEM_PROFILE` 控制加载哪个 settings 文件，默认 `develop`
- **数据库**: SQLite（`db.sqlite3`），已在 `.gitignore` 忽略，每台机器独立
- **核心依赖**: 只需 Django 5.1.2。requirements.txt 是全量 freeze 的，跨平台可能有不兼容的包（如 djangorestframework、django-cors-headers 等未使用但被 freeze 的包），装不上就单独 `pip install django`

## 常用命令

```bash
source .venv/bin/activate      # 激活虚拟环境
python manage.py runserver     # 启动开发服务器
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## URL 路由

| 路径 | name | 视图 |
|------|------|------|
| `/` | `index` | `IndexView` (ListView) |
| `/category/<category_id>/` | `category-list` | `CategoryView` |
| `/tag/<tag_id>/` | `tag-list` | `TagView` |
| `/post/<post_id>.html` | `post-detail` | `PostDetailView` (DetailView) |
| `/links/` | `links` | `links` |
| `/admin/` | — | `custom_site` 自定义管理后台 |
| `/super_admin/` | — | Django 原生 admin |

## 视图说明

- **IndexView**(CommonViewMixin, ListView): 首页，分页展示文章列表（每页 10 篇）
- **CategoryView**(IndexView): 继承首页，按分类过滤
- **TagView**(IndexView): 继承首页，按标签过滤
- **PostDetailView**(CommonViewMixin, DetailView): 文章详情
- **CommonViewMixin**: 为所有视图注入 `sidebars`、`navs`、`categories` 上下文
- 模板中用 `{% url 'name' %}` 反向解析 URL，避免硬编码路径

## 跨机协作注意事项

- 两台机器不要同时编辑同一文件，否则会产生合并冲突
- 每次开始工作前先 `git pull`，结束后 `git push`
- `db.sqlite3` 和 `.venv/` 不要提交
- 如果新增依赖，手动加到 `requirements.txt` 而不是全量 `pip freeze`
