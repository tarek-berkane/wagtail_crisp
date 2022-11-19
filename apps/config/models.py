from django.db import models
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting
class SocialMediaSettings(BaseSiteSetting):
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)


# Create your models here.


@register_setting
class WebsiteInfoSettings(BaseSiteSetting):
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


@register_setting
class GoogleAnalyticsSettings(BaseSiteSetting):
    is_enabled = models.BooleanField(default=False)
    account_id = models.CharField(max_length=50, blank=True, null=True)
