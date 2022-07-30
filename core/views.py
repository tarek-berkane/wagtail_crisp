from django.http import HttpRequest
from django.urls import reverse
from django.shortcuts import render


def page_not_found(request: HttpRequest, exception):
    return render(request, "404.html", status=404)


def server_error(request: HttpRequest, **kwargs):
    print(kwargs)
    return render(request, "500.html", status=500)



def robots(request):
    d = request.build_absolute_uri(reverse("sitemap"))

    return render(
        request,
        "robots.txt",
        content_type="text/plain",
        context={"sitemap_url": d},
    )
