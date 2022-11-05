import json
from datetime import datetime

from django.conf import settings
from django.urls import reverse
from django.contrib.sitemaps import ping_google
from django.core.management.base import BaseCommand

from core.settings.base import PING_FILE


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        FILE_NAME = settings.PING_FILE
        try:

            with open(PING_FILE, "r") as f:
                raw_data = f.read()

            data = json.loads(raw_data)

            if data["new_content"] == False:
                return

            # self.stdout.write(self.style.SUCCESS("Ping google"))
            ping_google(sitemap_url=reverse("sitemap"))

            data["new_content"] = False
            data["last_ping"] = str(datetime.now())
            json_data = json.dumps(data)

            with open(PING_FILE, "w") as f:
                f.write(json_data)

        except Exception:
            pass
