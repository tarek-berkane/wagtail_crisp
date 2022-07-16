from django.db import models

from wagtail.admin.panels import StreamFieldPanel, FieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.contrib.table_block.blocks import TableBlock

from apps.post.blocks import HeaderBlock, ImageBlock, QuoteBlock, CodeBlock


class CategoryIndex(Page):
    max_count = 1
    parent_page_types = ["home.Home"]
    subpage_types = ["post.PostCategory"]


class PostCategory(Page):
    parent_page_types = ["post.CategoryIndex"]
    subpage_types = ["post.Post"]


class Post(Page):
    parent_page_types = ["post.PostCategory"]

    RICH_TEXT_FEATURES = [
        "bold",
        "italic",
        "code",
        "ol",
        "ul",
        "link",
        "document-link",
    ]

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
