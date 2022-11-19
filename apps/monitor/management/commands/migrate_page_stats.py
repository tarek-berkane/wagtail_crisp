from django.core.management.base import BaseCommand, CommandError
from apps.monitor.services import migrate_page_statistics


class Command(BaseCommand):
    help = "Migrate page statistics from redis to django database"

    def handle(self, *args, **options):
        migrate_page_statistics()
