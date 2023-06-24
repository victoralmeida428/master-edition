from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CadastroForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            widget_attrs = field.widget.attrs
            widget_attrs['class'] = 'form-control mb-4'

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'email']