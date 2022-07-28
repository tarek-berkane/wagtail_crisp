from django.db import models
from django.core.paginator import Paginator

from wagtail.models import Page

from wagtail.contrib.routable_page.models import RoutablePageMixin, route


class ProjectIndex(RoutablePageMixin, Page):
    parent_page_types = ["home.Home"]
    subpage_types = ["post.Post"]
    max_count = 1

    @route(r"^$")
    def current_events(self, request):
        post = self.get_children().live()
        paginator = Paginator(post, 8)

        page_number = request.GET.get("p")
        if page_number:
            result = paginator.get_page(page_number)
        else:
            result = paginator.get_page(1)

        return self.render(
            request,
            context_overrides={
                "result": result,
            },
        )
