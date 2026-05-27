from django.http import HttpResponse
from django.views.generic import ListView

from blog.views import CommonViewMixin
from .models import Link

class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    tamplate_name = 'config/links.html'
    context_object_name = 'links_list'

def links(request):
    return HttpResponse('links')
