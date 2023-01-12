from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.db.models import Count, Sum

from redis.client import Redis
from django_redis import get_redis_connection


from apps.monitor.models import PageRequest
from apps.monitor.querysets import (
    get_last_day_page_visit,
    get_last_month_page_visit,
    get_last_week_page_visit,
    filter_only_page,
    filter_only_pages_dict,
)
from apps.monitor.utils import group_by_date, group_by_hour, page_request_count


def migrate_page_statistics():
    redis_client: Redis = get_redis_connection()
    service_name = settings.REDIS_PAGE_STATICS_SERVICE_NAME

    # this for redis old version
    page_stat = redis_client.zrange(service_name, 0, -1, withscores=True)
    redis_client.zremrangebyrank(service_name, 0, -1)

    # for new version it's better to use zpopmax
    # page_stat = redis_client.zpopmax(service_name, 1000)

    page_stat_instances = [
        PageRequest(page_name=item[0].decode(), count=item[1]) for item in page_stat
    ]

    PageRequest.objects.bulk_create(page_stat_instances)


def get_general_data_statistics(only_page=False):
    month_data = get_last_month_page_visit()
    week_data = get_last_week_page_visit(month_data)
    day_data = get_last_day_page_visit(month_data)

    if only_page:
        month_data = filter_only_page(month_data)
        week_data = filter_only_page(week_data)
        day_data = filter_only_page(day_data)

    data_group_by_month = group_by_date(month_data, timedelta(days=30))
    data_group_by_week = group_by_date(week_data, timedelta(days=7))
    data_group_by_day = group_by_hour(day_data)

    m = page_request_count(data_group_by_month)
    w = page_request_count(data_group_by_week)
    d = page_request_count(data_group_by_day)

    return {"month_data": m, "week_data": w, "day_data": d}


def get_top_pages(after_date: timezone = None, only_page=False):
    data = PageRequest.objects.all()
    if after_date:
        data = data.filter(create_date__gte=after_date)

    data = data.values("page_name").annotate(dcount=Sum("count"))

    if only_page:
        data = filter_only_pages_dict(data)

    return data
