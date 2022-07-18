from dataclasses import field
from django.forms import ModelForm

from apps.subscribe.models import SubscribeUser


class SubscribeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "revue-form-field"

    class Meta:
        model = SubscribeUser
        fields = ("user_email",)
