from django.apps import AppConfig


class PostConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.post"

    def ready(self) -> None:
        from wagtail.signals import page_published
        from apps.post.signals import update_content_tracker
        from apps.post.models import Post
        from django.conf import settings

        if not settings.DEBUG:
            page_published.connect(update_content_tracker, sender=Post)

