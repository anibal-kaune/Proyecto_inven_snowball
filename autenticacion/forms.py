from django import forms
from django.contrib.auth.forms import AuthenticationForm
from usuarios.models import Usuario

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'email', 'password', 'rol']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
