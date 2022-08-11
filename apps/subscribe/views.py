from functools import wraps
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from apps.subscribe.constants import ALREADY_SUBSCRIBE
from apps.subscribe.decorator import subscribe_limit

from apps.subscribe.forms import SubscribeForm


@require_http_methods(["POST"])
@subscribe_limit()
def subscribe(request: HttpRequest):
    form = SubscribeForm(request.POST)
    if form.is_valid():
        form.save()
    return HttpResponse("Done!")
