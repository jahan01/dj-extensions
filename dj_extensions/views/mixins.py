class PermissionsRequiredMixin(object):
    """
    For versions <1.9.
    Django >= 1.9 supports this by default.

    Mixin allows you to check for permission required to access the view
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
    Mixin which throws HttpResponseForbidden error if request is not a ajax
    """

    def dispatch(self, request, *args, **kwargs):
        if self.request.is_ajax():
            return super(AjaxOnlyMixin, self).dispatch(request, *args, **kwargs)
        else:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Invalid request.")

class PaginationMixin(object):
    """
    Mixin which allows List views to be paginated.
    Along with links to prev and next it provides a list of previous and proceeding n pages

    Add following to your template to place navingation links

    In your template:

        <nav>
          <ul class="pagination">
            {% if page_obj.has_previous %}
              <li><a href="?page={{ page_obj.previous_page_number }}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>
              {% for i in page_obj.paginator.page_range|slice:page_dict.prev %}
                <li><a href="?page={{ i }}">{{ i }}</a></li>
              {% endfor %}
            {% else %}
              <li><a href="javascript:;" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>
            {% endif %}
            <li class="active"><a href="javascript:;"> {{ page_obj.number }} <span class="sr-only">(current)</span></a></li>
            {% if page_obj.has_next %}
              {% for i in page_obj.paginator.page_range|slice:page_dict.next %}
                <li><a href="?page={{ i }}">{{ i }}</a></li>
              {% endfor %}
              <li><a href="?page={{ page_obj.next_page_number }}"><span aria-hidden="true">&raquo;</span></a></li>
            {% else %}
              <li><a href="javascript:;" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>
            {% endif %}
          </ul>
        </nav>
    """

    paginate_by = 5     # No. of objects to be listed in a page
    n_list = 4          # No. of previous and proceding pages to be included

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
    Mixin which allows List view to filter objects.
    Supply filtering condition as http query strings in your request.
    """

    allowed_filters = None

    """
    Example:
    Place this in your view

    allowed_filters = {
                       'name': 'emp_name__icontains',
                       'age' : 'age_exact',
                      }
    key is name of query string
    value is equivalent to filtering in Django ORM querysets
    """

    def get_queryset_filters(self):
        filters = {}

        for item in self.allowed_filters:
            if item in self.request.GET:
                filters[self.allowed_filters[item]] = self.request.GET[item]
        return filters

    def get_queryset(self):
        return super(FilterMixin, self).get_queryset().filter(**self.get_queryset_filters())