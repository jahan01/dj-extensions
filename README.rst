.. |copy|    unicode:: U+000A9 .. COPYRIGHT SIGN

.. image:: https://travis-ci.org/jahan01/dj-extensions.svg?branch=master
    :target: https://travis-ci.org/jahan01/dj-extensions
    :alt: master build

.. image:: https://badge.fury.io/py/dj-extensions.svg
    :target: https://badge.fury.io/py/dj-extensions

.. image:: https://coveralls.io/repos/github/jahan01/dj-extensions/badge.svg?branch=master
    :target: https://coveralls.io/github/jahan01/dj-extensions?branch=master

.. image:: https://codecov.io/github/jahan01/dj-extensions/coverage.svg?branch=master
    :target: https://codecov.io/github/jahan01/dj-extensions?branch=master

.. image:: https://readthedocs.org/projects/dj-extensions/badge/?version=latest
    :target: http://dj-extensions.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: http://readthedocs.org/projects/dj-extensions/badge/?version=stable
    :target: http://dj-extensions.readthedocs.org/en/stable/?badge=stable
    :alt: Documentation Status

.. image:: http://img.shields.io/badge/license-MIT-brightgreen.svg
    :target: http://opensource.org/licenses/MIT

**Copyright** |copy| **2016 Jahan Balasubramaniam**

Django Extensions
=================

**dj-extensions**


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
        paginate_by          = 10
        n_list               = 5
        required_permissions = (
                                'app.permission1',
                                'app.permission2',
                               )
        allowed_filters      = {
                                'name': 'emp_name__icontains',
                                'age' : 'age_exact',
                               }

**Source code:** Find the source code at `github repo`_

**Documentation:** Find the docs at `readthedocs`_

*For different versions:*

- `stable release`_
- `latest version`_

To install latest version, which will not be available in pypi, run below

::

    pip install --upgrade https://github.com/jahan01/dj-extensions/tree/master

**License: MIT**

.. _readthedocs: http://dj-extensions.readthedocs.org/
.. _github repo: https://github.com/jahan01/dj-extensions
.. _stable release: http://dj-extensions.readthedocs.org/en/stable/index.html
.. _latest version: http://dj-extensions.readthedocs.org/en/latest/index.html
