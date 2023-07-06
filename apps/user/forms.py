from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User


class CadastroForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            widget_attrs = field.widget.attrs
            widget_attrs['class'] = 'form-control mb-4'

    class Meta(UserCreationForm.Meta):
        fields = ['first_name', 'last_name','username', 'password1', 'password2', 'email']

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            widget_attrs = field.widget.attrs
            widget_attrs['class'] = 'form-control mb-4'

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            user = User.objects.get(username=username)
            print(user.check_password(password))
            if not user.check_password(password):
                self.add_error('password', 'Senha incorreta')
        except User.DoesNotExist:
            self.add_error('username', 'Usuário inválido')

        return cleaned_data

class ChangePassowrdForm(PasswordChangeForm):
    fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            widget_attrs = field.widget.attrs
            widget_attrs['class'] = 'form-control mb-4'

class PerfilForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            widget_attrs = field.widget.attrs
            widget_attrs['class'] = 'form-control mb-4'

    username = forms.CharField(label='Usuário', required=False)
    first_name = forms.CharField(label='Primeiro Nome', required=False)
    last_name = forms.CharField(label='Último Nome', required=False)
    email = forms.EmailField(label='E-mail', required=False)

class PixForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            widget_attrs = field.widget.attrs
            widget_attrs['class'] = 'form-control mb-4'
    
    choices = ((5,'5,00'),(10,'10,00'), (15,'15,00'), (25,'25,00'), (50,'50,00'))
    doacao = forms.ChoiceField(choices=choices, label='Doação (R$)')



