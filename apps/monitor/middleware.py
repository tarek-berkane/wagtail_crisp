from django.http import HttpRequest
from django.urls import resolve

from apps.monitor.utils import increment_page_startcis_for_users


def statics_middleware(get_response):
    def middleware(request: HttpRequest):
        increment_page_startcis_for_users(request)
        response = get_response(request)
        return response

    return middleware
