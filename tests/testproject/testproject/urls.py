from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.auth import views as auth_views
from testapp.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', auth_views.login, {'template_name': 'dummy.html'}, name='login'),

    url(r'^permission_required/$', PermissionView.as_view(), name='permission_required'),
    url(r'^multiple_permission_required/$', MultiplePermissionView.as_view(), name='multiple_permission_required'),
    url(r'^ajax_only/$', AjaxOnlyView.as_view(), name='ajax_only'),
    url(r'^filter_view/$', FilterView.as_view(), name='filter_view'),
    url(r'^paginated_view/$', PaginatedView.as_view(), name='paginated_view'),
]
