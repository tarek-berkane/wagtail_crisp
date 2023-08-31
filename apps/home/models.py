from django.db import models
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route


from apps.post.models import Post, PostCategory
from apps.project.models import ProjectIndex

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


# class HomePage(Page):
#     pass


# @method_decorator(cache_page_if_not_preview, name="serve")
class HomePage(RoutablePageMixin, Page):
    max_count = 1

    @route(r"^$")
    def current_events(self, request):
        context = {}

        post_type = request.GET.get("post-type")
        post_type = post_type or "all"
        tag = request.GET.get("tag")
        page_number = request.GET.get("p")

        queryset = self.get_queryset(post_type, tag)
        result = self.get_reuslt_pagination(queryset, page_number)

        context["result"] = result
        context["post_type"] = post_type
        context["url_parameter"] = self.build_url_parameter(post_type, tag)

        return self.render(request, context_overrides=context)

    def get_queryset(self, post_type, tag):

        post = Post.objects.all().live().order_by('-first_published_at')

        if post_type == "post":
            parent_type = PostCategory.objects.first()
            if parent_type:
                post = post.child_of(parent_type)

        elif post_type == "project":
            parent_type = ProjectIndex.objects.first()
            if parent_type:
                post = post.child_of(parent_type)

        if tag:
            post = post.filter(tags__name=tag)

        return post

    def get_reuslt_pagination(self, queryset, page_number):
        paginator = Paginator(queryset, 8)

        if page_number:
            result = paginator.get_page(page_number)
        else:
            result = paginator.get_page(1)

        return result

    def build_url_parameter(self, post_type, tag):
        parameter = ""
        if post_type:
            parameter += f"post-type={post_type}&"
        if tag:
            parameter += f"tag={tag}&"

        return parameter


@method_decorator(cache_page_if_not_preview, name="serve")
class Author(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]

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
            [
                FieldPanel("auth_image"),
                FieldPanel("full_name"),
            ],
            heading="Main info",
        ),
        FieldPanel("content"),
    ]


# FORMS
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")


@method_decorator(cache_page_if_not_preview, name="serve")
class FormPage(WagtailCaptchaEmailForm):
    max_count = 1

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("intro", classname="full"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text", classname="full"),
    ]
