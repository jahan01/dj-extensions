__&copy; 2016 Jahan Balasubramaniam__

# Django Extensions
###### dj-extensions

Yet another Django extension with set of generic reusable, pluggable mixins

##### Installation

```
pip install dj-extensions
```

######
__Currently includes following Mixins:__

* PermissionsRequiredMixin
* AjaxOnlyMixin
* PaginationMixin
* FilterMixin

__Usage:__
```python
from dj_extensions.views import PermissionsRequiredMixin, FilterMixin, PaginationMixin

class SomeView(PermissionsRequiredMixin, FilterMixin, PaginationMixin, ListView):
    model                = <Your Model>
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
```

___Source code:___ Find the source code [here](https://github.com/jahan01/dj-extensions) at github

___Documentation:___ To be done. For now, please refer to the comments in the source code.

__License: MIT__