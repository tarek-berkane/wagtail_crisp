from functools import wraps
from django.http import HttpRequest, HttpResponseBadRequest


def subscribe_limit():
    """
    Decorator to limit number of time the user can subscribe.  Usage::
    """

    def decorator(func):
        @wraps(func)
        def inner(request: HttpRequest, *args, **kwargs):
            if subscribe_count := request.session.get("subscribe_count"):
                if subscribe_count > 3:
                    return HttpResponseBadRequest()
                count = request.session["subscribe_count"] + 1
            else:
                count = 1
            request.session["subscribe_count"] = count
            return func(request, *args, **kwargs)

        return inner

    return decorator
