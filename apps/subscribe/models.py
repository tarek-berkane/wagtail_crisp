from django.db import models

# Create your models here.
class SubscribeUser(models.Model):
    user_email = models.EmailField("email")
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user_email
