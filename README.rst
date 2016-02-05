.. |copy|    unicode:: U+000A9 .. COPYRIGHT SIGN

**Copyright** |copy| **2016 Jahan Balasubramaniam**

Django Extensions
=================

dj-extensions


Yet another Django extension with set of generic reusable, pluggable mixins

Installation
''''''''''''

::

    pip install dj-extensions

**Currently includes following Mixins:**

-  PermissionsRequiredMixin
-  AjaxOnlyMixin
-  PaginationMixin
-  FilterMixin

**Usage:**

.. code:: python

    from dj_extensions.views import PermissionsRequiredMixin, FilterMixin, PaginationMixin

    class SomeView(PermissionsRequiredMixin, FilterMixin, PaginationMixin, ListView):
        model                = YourModel
        paginated_by         = 10
        n_list               = 5
        required_permissions = (
                                'app.permission1',
                                'app.permission2',
                               )
        allowed_filters      = {
                                'name': 'emp_name__icontains',
                                'age' : 'age_exact',
                               }

**Source code:** Find the source code `here`_ at github

**Documentation:** To be done. For now, please refer to the comments in the source code.

**License: MIT**

.. _here: https://github.com/jahan01/dj-extensions