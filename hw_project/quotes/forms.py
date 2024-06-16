from django import forms
from .models import User

class Meta:
    model = User
    fields = ('username', 'email', 'password', 'confirm_password')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')