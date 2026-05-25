from blogsystem.base_admin import BaseOwnerAdmin
from blogsystem.custom_site import custom_site
from .models import Link, SideBar


class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time',)
    fields = ('title', 'href', 'status', 'weight',)


class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display', 'content', 'created_time')
    fields = ('title', 'display', 'content')


custom_site.register(Link, LinkAdmin)
custom_site.register(SideBar, SideBarAdmin)
