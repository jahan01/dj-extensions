View Mixins
===========

These mixins provide additional fuunctionality to django class based views.

Currently following mixins are supported.
This list will be expanding over the time. Kindly keep check on it.

Mixin names explain roughly what they do.

.. contents::

.. _PermissionRequiredMixin:

PermissionRequiredMixin
-----------------------

**Usage:**

.. code-block:: python

    from django.views.generic import ListView
    from dj_extensions.views import PermissionsRequiredMixin

    class SomeView(PermissionsRequiredMixin, ListView):
        model                = YourModel
        required_permissions = ('app.permission1')

You can check for more than one permission too

.. code-block:: python

    from django.views.generic import ListView
    from dj_extensions.views import PermissionsRequiredMixin

    class SomeView(PermissionsRequiredMixin, ListView):
        model                = YourModel
        required_permissions = ('app.permission1',
                                'app.permission2',
                            )

The variable `required_permissions` is required.

.. note::
    No need to check for do login required check if you are doing permissions checks. In either case if the check fails, the user will be redirected to login page


.. _AjaxOnlyMixin:

AjaxOnlyMixin
-------------

This mixin allows only the ajax requests and returns HttpForbiddenError if the request is not ajax.

**Usage:**

.. code-block:: python

    from django.views.generic import TemplateView
    from dj_extensions.views import AjaxOnlyMixin

    class SomeView(AjaxOnlyMixin, TemplateView):
        # your custom code

.. _PaginationMixin:

PaginationMixin
---------------

This mixin provides list of links to previous and next `n` number of pages, in addition to just previous and next links provided by default.

**Usage:**

.. code:: python

    from django.views.generic import ListView
    from dj_extensions.views import PaginationMixin

    class SomeView(PaginationMixin, ListView):
        model                = YourModel
        paginated_by         = 10
        n_list               = 5

In your template for this view, add the following lines:

.. code-block:: django

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

.. note::
    This mixin only works with List views.


.. _FilterMixin:

FilterMixin
-----------

This mixin is used filter your list view based on query strings from http requests

**Usage:**

.. code-block:: python

    from django.views.generic import ListView
    from dj_extensions.views import FilterMixin

    class SomeView(FilterMixin, ListView):
        model                = YourModel
        allowed_filters      = {
                                'name': 'emp_name__icontains',
                                'age' : 'age_exact',
                               }


The key of the `allowed_filters` dict is the query string and value is the django ORM filter opertation.

For example, the request `http://localhost:8000/some_view?name=foo&age=21` will perform

::

    yourmodel.objects.filter(emp_name_icontains='foo').filter(age_exact=21)


.. note::
    This mixin only works with List views.