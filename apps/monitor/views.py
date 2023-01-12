# Create your views here.
from datetime import datetime, timedelta
from typing import List

from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from apps.monitor.models import PageRequest
from apps.monitor.services import get_general_data_statistics, get_top_pages


# def get_last_24_static():
#     now = timezone.now()
#     yesterday = now - timedelta(days=1)
#     data = PageRequest.objects.filter(create_date__gte=yesterday)
#     return aggregate_by_time(data, yesterday)


# def aggregate_by_time(data, yesterday):
#     result = []

#     time = yesterday

#     for i in range(25):
#         result.append([time, 0])
#         time = time + timedelta(hours=1)

#     for item in data:
#         for r in result:
#             if r[0].hour == item.create_date.hour and r[0].day == item.create_date.day:
#                 r[1] += item.count
#                 continue

#     return result


# def get_last_month():
#     now = timezone.now()
#     last_moth = now - timedelta(days=30)
#     data = PageRequest.objects.filter(create_date__gte=last_moth)
#     return aggregate_by_day(data, last_moth)


# def aggregate_by_day(data, last_month):
#     result = []

#     time = last_month
#     today = timezone.now()

#     for i in range(40):
#         if time > today:
#             break

#         result.append([time, 0])
#         time = time + timedelta(days=1)

#     for item in data:
#         for r in result:
#             if (
#                 r[0].month == item.create_date.month
#                 and r[0].day == item.create_date.day
#             ):
#                 r[1] += item.count
#                 continue

#     return result


def index(request):
    return render(
        request,
        "admin/monitor/live_static.html",
    )


@cache_page(60 * 20)
def top_pages(request):
    only_page = False
    if request.GET.get("only_page") == "true":
        only_page = True

    yesterday = get_top_pages(timezone.now() - timedelta(days=1), only_page=only_page)
    yesterday = yesterday[:10]

    last_week = get_top_pages(timezone.now() - timedelta(days=7), only_page=only_page)
    last_week = last_week[:10]

    last_month = get_top_pages(timezone.now() - timedelta(days=30), only_page=only_page)
    last_month = last_month[:10]

    return render(
        request,
        "admin/monitor/top_pages.html",
        context={
            "yesterday": yesterday,
            "last_week": last_week,
            "last_month": last_month,
        },
    )


@cache_page(60 * 20)
def page_visit_data(request):
    only_page = False
    if request.GET.get("only_page") == "true":
        only_page = True
    data = get_general_data_statistics(only_page=only_page)
    return JsonResponse(data=data)
