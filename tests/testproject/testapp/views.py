from .models import *

from dj_extensions.views import PermissionsRequiredMixin, FilterMixin, PaginationMixin, AjaxOnlyMixin
from django.views.generic import View, TemplateView, ListView
from django.http import HttpResponse


class BaseView(View):

    def get(self, request):
        return HttpResponse("Success Get")

    # def post(self, request):
    #     return HttpResponse("Success Post")

class PermissionView(PermissionsRequiredMixin, BaseView):

    required_permissions = (
                            'testapp.add_sample',
                           )

class MultiplePermissionView(PermissionsRequiredMixin, BaseView):

    required_permissions = (
                            'testapp.add_sample',
                            'testapp.change_sample',
                           )

class AjaxOnlyView(AjaxOnlyMixin, BaseView):
    """
    To check AjaxOnlyMixin
    """

class FilterView(FilterMixin, ListView):
    model               = Sample
    template_name       = 'dummy.html'
    allowed_filters     = {
                            'string' : 'field1__icontains',
                            'number' : 'field2__exact',
                        }

    def get_context_data(self, **kwargs):
        context = super(FilterView, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context

    def get(self, request, *args, **kwargs):
        listview = super(FilterView, self).get(request, *args, **kwargs)
        count = listview.context_data['count']
        return HttpResponse("Count %s" % count)

class PaginatedView(PaginationMixin, ListView):

    paginate_by   = 1
    n_list        = 5
    model         = Sample
    template_name = 'dummy.html'

    def get(self, request, *args, **kwargs):
        listview = super(PaginatedView, self).get(request, *args, **kwargs)
        page_dict = listview.context_data['page_dict']
        return HttpResponse("Page dict: %s" % page_dict)
