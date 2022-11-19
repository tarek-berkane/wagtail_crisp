from datetime import datetime, timedelta
from typing import List

from django.utils import timezone
from django.conf import settings
from django.http import HttpRequest

from django_redis import get_redis_connection
from redis.client import Redis

from apps.monitor.models import PageRequest


def same_day(date_1: datetime, date_2: datetime):
    if (
        date_1.day == date_2.day
        and date_1.month == date_2.month
        and date_1.year == date_2.year
    ):
        return True
    return False


def same_day_hour(date_1: datetime, date_2: datetime):
    if same_day(date_1, date_2):
        if date_1.hour == date_2.hour:
            return True
    return False


def group_by_date(data, time_interval):
    result = {}

    today = timezone.now()
    interval: datetime = today - time_interval

    while True:
        if interval > today:
            break

        current_time = interval.strftime("%Y-%m-%d")
        result[current_time] = []

        for index in range(len(data)):
            if same_day(interval, data[index].create_date):
                result[current_time].append(data[index])
                # TODO: NEED TO REFACTOR

        interval = interval + timedelta(days=1)

    return result


def group_by_hour(data):
    result = {}

    today_plus_1h = timezone.now() + timedelta(hours=1)
    yesterday: datetime = today_plus_1h - timedelta(days=1)

    while True:
        if yesterday > today_plus_1h:
            break

        current_time = f"{yesterday.hour}:00"
        result[current_time] = []

        for index in range(len(data)):
            if same_day_hour(yesterday, data[index].create_date):
                result[current_time].append(data[index])
                # TODO: NEED TO REFACTOR

        yesterday = yesterday + timedelta(hours=1)

    return result


def page_request_in_day_by_page(data: List[PageRequest]):
    result = {}
    for item in data:
        if n := result.get(item.page_name):
            result[item.page_name] += item.count
        else:
            result[item.page_name] = item.count

    return result


def page_request_count_by_page(data: dict):
    for key, value in data.items():
        data[key] = page_request_in_day_by_page(value)

    return data


def page_request_count(data: dict):
    for key, value in data.items():
        data[key] = sum(page_request_in_day_by_page(value).values())

    return data


def increment_page_statics(request):
    redis_client: Redis = get_redis_connection()
    page_path = request.path
    print("register path", page_path)
    service_name = settings.REDIS_PAGE_STATICS_SERVICE_NAME

    redis_client.zadd(service_name, {page_path: 1}, incr=True)


def increment_page_startcis_for_users(request: HttpRequest):
    if request.user.is_anonymous:
        increment_page_statics(request)
