# blogsystem — Django 博客系统

## 项目结构

```
blogsystem/          # Django 项目配置（settings, urls, wsgi）
  settings/
    base.py          # 公共配置（SQLite, 中文, 上海时区）
    develop.py       # 开发环境（DEBUG=True）
blog/                # 博客 APP — Post, Category, Tag 模型
comment/             # 评论 APP
config/              # 配置 APP — 友情链接等
```

## 环境配置

- **Python**: 3.13（Mac）/ 3.x（Windows），各机器独立管理 `.venv`
- **配置切换**: 通过环境变量 `BLOGSYSTEM_PROFILE` 控制加载哪个 settings 文件，默认 `develop`
- **数据库**: SQLite（`db.sqlite3`），已在 `.gitignore` 忽略，每台机器独立
- **依赖安装**: `pip install -r requirements.txt`（注意：目前 requirements.txt 是全量 freeze 的，跨平台可能有版本不兼容的包，核心依赖只需 Django 5.1.2、djangorestframework 3.15.2、django-cors-headers 4.4.0 等）

## 常用命令

```bash
source .venv/bin/activate      # 激活虚拟环境
python manage.py runserver     # 启动开发服务器
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## URL 路由

| 路径 | 说明 |
|------|------|
| `/` | 文章列表 |
| `/category/<id>/` | 按分类筛选 |
| `/tag/<id>/` | 按标签筛选 |
| `/post/<id>.html` | 文章详情 |
| `/links/` | 友情链接 |
| `/admin/` | 自定义管理后台 |
| `/super_admin/` | Django 原生 admin |

## 跨机协作注意事项

- 两台机器不要同时编辑同一文件，否则会产生合并冲突
- 每次开始工作前先 `git pull`，结束后 `git push`
- `db.sqlite3` 和 `.venv/` 不要提交
- 如果新增依赖，手动加到 `requirements.txt` 而不是全量 `pip freeze`
