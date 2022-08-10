from functools import wraps
from django.http import HttpRequest, HttpResponseBadRequest

from apps.subscribe.constants import ALREADY_SUBSCRIBE, SUBSCRIBE_COUNT


def subscribe_limit():
    """
    Decorator to limit number of time the user can subscribe.  Usage::
    """

    def decorator(func):
        @wraps(func)
        def inner(request: HttpRequest, *args, **kwargs):
            if subscribe_count := request.session.get(SUBSCRIBE_COUNT):
                if subscribe_count > 3:
                    request.session[ALREADY_SUBSCRIBE] = True
                    return HttpResponseBadRequest()
                count = request.session[SUBSCRIBE_COUNT] + 1
            else:
                count = 1
            request.session[SUBSCRIBE_COUNT] = count

            return func(request, *args, **kwargs)

        return inner

    return decorator
