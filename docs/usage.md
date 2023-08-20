# Usage

This library is meant for situations where you need to do some special
handling whenever data is returned though the Django ORM. Some possible
use cases might be:

- Audit logging
- Obfuscation
- Checking permissions
- Validating
- Enhancing

You might have been considering Django's [pre_init] or [post_init] signals,
but realized that they do not work when using `.values()` or `.values_list()`.
Signals can also be [hard to maintain] and can be [overridden] on accident.

This isn't to say that using the post-fetch hooks offered by this library
are strictly better. For instance, it does not fire on [queryset.iterator()][iter]
due to implementation details, so it that's a requirement, signals might
be a better alternative.

If you're interested, here is what you would implement the hooks on your models:

```python
from typing import Any
from post_fetch_hook.models import PostFetchModel

class MyModel(PostFetchModel):

    # You can implement any of these methods.
    # These are their default configurations.

    @classmethod
    def post_fetch_hook(cls, model: "MyModel") -> "MyModel":
        # Special handling
        return model

    @classmethod
    def post_fetch_values_hook(cls, values: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
        # Special handling
        return values

    @classmethod
    def post_fetch_values_list_hook(cls, values: tuple[Any, ...], fields: tuple[str, ...]) -> tuple[Any, ...]:
        # Special handling
        return values

    @classmethod
    def post_fetch_values_list_flat_hook(cls, value: Any, field: str) -> Any:
        # Special handling
        return value
```

You can also use the included mixins (`PostFetchQuerySetMixin` and `PostFetchModelMixin`)
to build the functionality in your custom models.

> When using custom models, remember to set `base_manager_name = "objects"`
> (given that "objects" points to the manager with the post fetch functionality)
> in the model Meta-class so that post fetch hooks are fired on related entities.


[pre_init]: https://docs.djangoproject.com/en/dev/ref/signals/#pre-init
[post_init]: https://docs.djangoproject.com/en/dev/ref/signals/#post-init
[hard to maintain]: https://docs.djangoproject.com/en/dev/ref/signals/#post-init:~:text=Warning-,Signals%20can%20make%20your%20code%20harder%20to%20maintain.,-Consider%20implementing%20a
[overridden]: https://docs.djangoproject.com/en/dev/ref/signals/#post-init:~:text=Many%20of%20these,to%20be%20sent.
[iter]: https://docs.djangoproject.com/en/dev/ref/models/querysets/#iterator
