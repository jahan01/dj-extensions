class PermissionsRequiredMixin(object):
    """
    For django versions <1.9.\n
    django >= 1.9 supports this by default.

    Mixin checks for required permissions for the view to authenticate users.
    """

    required_permissions = None # string or list/tuple of string stating required permission to access the view
                                # Add this in you view class

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms(self.required_permissions):
            from django.utils.six.moves.urllib.parse import urlparse
            from django.conf import settings
            from django.shortcuts import resolve_url
            from django.contrib.auth import REDIRECT_FIELD_NAME
            from django.contrib.auth.views import redirect_to_login

            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(settings.LOGIN_URL)
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]

            if ((not login_scheme or login_scheme == current_scheme) and (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)
        return super(PermissionsRequiredMixin, self).dispatch(request, *args, **kwargs)

class AjaxOnlyMixin(object):
    """
    Mixin throws HttpResponseForbidden error if request is not ajax.
    """

    def dispatch(self, request, *args, **kwargs):
        if self.request.is_ajax():
            return super(AjaxOnlyMixin, self).dispatch(request, *args, **kwargs)
        else:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Invalid request.")

class PaginationMixin(object):
    """
    Mixin for google style paginations.
    """

    paginate_by = 5     # No. of objects to be listed in a page
    n_list      = 4     # No. of previous and proceding pages to be included in pagenation object

    def get_context_data(self, **kwargs):
        context = super(PaginationMixin, self).get_context_data(**kwargs)
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        page_number = int(page)
        page_dict = {}

        if page_number <= self.n_list:
            page_dict['prev'] = "0:" + str(page_number-1)
        else:
            page_dict['prev'] = str(page_number-self.n_list-1) + ":" + str(page_number-1)

        page_dict['next'] = str(page_number) + ":" + str(page_number+self.n_list)
        context['page_dict'] = page_dict
        return context

class FilterMixin(object):
    """
    Mixin for filtering List view based on http request query strings.
    """

    allowed_filters = None

    def get_queryset_filters(self):
        filters = {}

        for item in self.allowed_filters:
            if item in self.request.GET:
                filters[self.allowed_filters[item]] = self.request.GET[item]
        return filters

    def get_queryset(self):
        return super(FilterMixin, self).get_queryset().filter(**self.get_queryset_filters())
