from django.db import models
from django.core.paginator import Paginator

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from wagtail.contrib.routable_page.models import RoutablePageMixin, route


RICH_TEXT_FEATURES = [
    "bold",
    "italic",
    "code",
    "ol",
    "ul",
    "link",
    "document-link",
]


class ProjectIndex(RoutablePageMixin, Page):
    parent_page_types = ["home.Home"]
    subpage_types = ["post.Post"]
    max_count = 1

    description = RichTextField(features=RICH_TEXT_FEATURES, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

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
