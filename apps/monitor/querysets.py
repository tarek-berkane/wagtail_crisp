from typing import List, Optional
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django.urls import resolve

from apps.monitor.models import PageRequest


def get_page_visit_by_interval(date_from, date_to):
    data = PageRequest.objects.filter(
        Q(create_date__lte=date_from) and Q(create_date__gte=date_to)
    )
    return data


def get_last_page_visit(
    data: Optional[List[PageRequest]] = None, interval_days=timedelta(days=1)
):
    today = timezone.now()
    interval = today - interval_days
    if not data:
        page_visit_data = get_page_visit_by_interval(today, interval)
    else:
        page_visit_data = []

        for item in data:
            if item.create_date > interval:
                page_visit_data.append(item)

    return page_visit_data


def get_last_day_page_visit(extract_from: Optional[List[PageRequest]] = None):
    return get_last_page_visit(extract_from)


def get_last_week_page_visit(extract_from: Optional[List[PageRequest]] = None):
    return get_last_page_visit(extract_from, interval_days=timedelta(days=7))


def get_last_month_page_visit(extract_from: Optional[List[PageRequest]] = None):
    return get_last_page_visit(extract_from, interval_days=timedelta(days=30))


def filter_only_page(data: List[PageRequest]):
    filtered_data = []
    for page in data:
        match = resolve(page.page_name)
        if match.url_name == "wagtail_serve":
            filtered_data.append(page)

    return filtered_data


def filter_only_pages_dict(data: List[dict]):
    filtered_data = []
    for page in data:
        match = resolve(page["page_name"])
        if match.url_name == "wagtail_serve":
            filtered_data.append(page)

    return filtered_data
