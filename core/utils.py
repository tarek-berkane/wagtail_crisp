import logging


from django.http import HttpRequest
from django.views.decorators.cache import cache_page, never_cache


logger = logging.getLogger("django")

DEFAULT_CACHE_TIME = 60 * 10


def cache_page_if_not_preview(func):
    def test_priview(request: HttpRequest, *args, **kwargs):
        print(request.path)
        is_preview = getattr(request, "is_preview", False)
        if is_preview:
            logger.info("didn't cache")
            return never_cache(func)(request, *args, **kwargs)

        if request.user.is_anonymous:
            logger.info("page cached")
            return cache_page(DEFAULT_CACHE_TIME, key_prefix="cached")(func)(
                request, *args, **kwargs
            )
        else:
            logger.info("User is loged don't cache this")
            return func(request, *args, **kwargs)

    return test_priview
