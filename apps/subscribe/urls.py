from django.urls import path

from apps.subscribe.views import subscribe


urlpatterns = [
    path("", subscribe, name="subscribe-view"),
]
