from django.urls import path, reverse

from wagtail.admin.menu import MenuItem, SubmenuMenuItem
from wagtail.contrib.modeladmin.menus import Menu
from wagtail.core import hooks


from apps.monitor.views import index, page_visit_data, top_pages


@hooks.register("register_admin_urls")
def register_calendar_url():
    return [
        path("monitor/", index, name="monitor"),
        path("monitor-page-visit-data", page_visit_data, name="page-visit-data"),
        path("monitor-top-pages/", top_pages, name="top-pages"),
    ]


@hooks.register("register_admin_menu_item")
def register_calendar_menu_item():
    menu_items = [
        MenuItem("monitor", reverse("monitor")),
        MenuItem("top pages", reverse("top-pages")),
    ]

    return SubmenuMenuItem("Monitor", Menu(items=menu_items))
