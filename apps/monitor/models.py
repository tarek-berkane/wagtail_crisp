from itertools import count
from venv import create
from django.db import models

# Create your models here.


class PageRequest(models.Model):
    page_name = models.CharField(max_length=500)
    count = models.PositiveIntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.page_name} | {self.count} | {self.create_date}"
