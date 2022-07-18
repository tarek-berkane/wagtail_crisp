from django.shortcuts import render
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponse

from apps.subscribe.forms import SubscribeForm

# Create your views here.


def subscribe(requests: HttpRequest):
    if requests.POST:
        form = SubscribeForm(requests.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Done!")
    else:
        return HttpResponseBadRequest()
