from django.db import models

from wagtail.admin.panels import StreamFieldPanel, FieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.blocks import RichTextBlock
from wagtail.contrib.table_block.blocks import TableBlock

from apps.post.blocks import HeaderBlock, ImageBlock, QuoteBlock, CodeBlock

RICH_TEXT_FEATURES = [
    "bold",
    "italic",
    "code",
    "ol",
    "ul",
    "link",
    "document-link",
]


class CategoryIndex(Page):
    max_count = 1
    parent_page_types = ["home.Home"]
    subpage_types = ["post.PostCategory"]


class PostCategory(Page):
    parent_page_types = ["post.CategoryIndex"]
    subpage_types = ["post.Post"]

    description = RichTextField(features=RICH_TEXT_FEATURES, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]


class Post(Page):
    parent_page_types = ["post.PostCategory"]

    content = StreamField(
        [
            ("head", HeaderBlock()),
            ("blockquote", QuoteBlock()),
            ("rich_text", RichTextBlock(features=RICH_TEXT_FEATURES)),
            ("image", ImageBlock()),
            ("table", TableBlock()),
            ("code", CodeBlock()),
        ]
    )

    content_panels = Page.content_panels + [FieldPanel("content")]
