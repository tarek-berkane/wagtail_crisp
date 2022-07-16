from django.db import models

from wagtail.models import Page
from wagtail.core.fields import RichTextField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.panels import MultiFieldPanel, FieldPanel

from apps.post.models import Post

RICH_TEXT_FEATURES = [
    "bold",
    "italic",
    "code",
    "ol",
    "ul",
    "link",
    "document-link",
]


class Home(Page):
    max_count = 1

    def lates_posts(self):
        posts = Post.objects.all().live()
        return posts


class Author(Page):
    max_count = 1
    parent_page_types = ["home.Home"]

    auth_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )

    full_name = models.CharField(max_length=50)
    content = RichTextField(features=RICH_TEXT_FEATURES)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("auth_image"), FieldPanel("full_name")], heading="Main info"
        ),
        FieldPanel("content"),
    ]


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)


# Create your models here.


@register_setting
class WebsiteInfoSettings(BaseSetting):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=25, default="Website")
    description = models.CharField(max_length=255, default="Change this text")
