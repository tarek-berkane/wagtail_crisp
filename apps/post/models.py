from django.db import models
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.blocks import RichTextBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from apps.post.blocks import HeaderBlock, ImageBlock, QuoteBlock, CodeBlock
from apps.subscribe.constants import ALREADY_SUBSCRIBE
from apps.subscribe.forms import SubscribeForm
from apps.subscribe.services import already_subscribed

from core.utils import cache_page_if_not_preview

RICH_TEXT_FEATURES = [
    "bold",
    "italic",
    "code",
    "ol",
    "ul",
    "link",
    "document-link",
]


class PostPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "Post", related_name="tagged_items", on_delete=models.CASCADE
    )


@method_decorator(cache_page_if_not_preview, name="serve")
class CategoryIndex(RoutablePageMixin, Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = ["post.PostCategory"]

    @route(r"^$")
    def current_events(self, request):
        post = PostCategory.objects.all().live()
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


@method_decorator(cache_page_if_not_preview, name="serve")
class PostCategory(RoutablePageMixin, Page):
    parent_page_types = ["post.CategoryIndex"]
    subpage_types = ["post.Post"]

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


@method_decorator(cache_page_if_not_preview, name="serve")
class Post(Page):
    parent_page_types = ["post.PostCategory", "project.ProjectIndex"]
    tags = ClusterTaggableManager(through=PostPageTag, blank=True)

    include_comments = models.BooleanField(default=True)

    content = StreamField(
        [
            ("head", HeaderBlock()),
            ("blockquote", QuoteBlock()),
            ("rich_text", RichTextBlock(features=RICH_TEXT_FEATURES)),
            ("image", ImageBlock()),
            ("table", TableBlock()),
            ("code", CodeBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("tags"),
        FieldPanel("content"),
    ]

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("include_comments"),
            ],
            heading="comments",
        )
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["form"] = SubscribeForm()
        context[ALREADY_SUBSCRIBE] = already_subscribed(request)
        return context
