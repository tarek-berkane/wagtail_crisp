from django.http import HttpRequest

from apps.subscribe.constants import ALREADY_SUBSCRIBE


def already_subscribed(request: HttpRequest):
    if request.session.get(ALREADY_SUBSCRIBE):
        return True
    return False
