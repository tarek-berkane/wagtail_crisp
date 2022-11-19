from django.http import HttpRequest

from apps.monitor.utils import increment_page_statics


def page_statistics(func):
    def test_priview(request: HttpRequest, *args, **kwargs):
        increment_page_statics(request)
        return func(request, *args, **kwargs)

    return test_priview
