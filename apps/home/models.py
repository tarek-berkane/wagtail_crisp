from xml.etree.ElementInclude import include
from django.db import models
from django.core.paginator import Paginator

from wagtail.models import Page
from wagtail.core.fields import RichTextField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

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


class Home(RoutablePageMixin, Page):
    max_count = 1

    @route(r"^$")
    def current_events(self, request):
        context = {}
        post = Post.objects.all().live()

        tag = request.GET.get("tag")
        if tag:
            post = post.filter(tags__name=tag)
            context["tag_url"] = f"tag={tag}&"

        paginator = Paginator(post, 8)

        page_number = request.GET.get("p")
        if page_number:
            result = paginator.get_page(page_number)
        else:
            result = paginator.get_page(1)

        context["result"] = result

        return self.render(request, context_overrides=context)


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
    side_logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )

    text_logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )

    website_name = models.CharField(max_length=25, default="Website")
    website_description = models.CharField(max_length=255, default="Change this text")
    disqus_url = models.URLField(null=True, blank=True)


# FORMS
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")


class FormPage(WagtailCaptchaEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("intro", classname="full"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text", classname="full"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]
