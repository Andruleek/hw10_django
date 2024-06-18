from django import forms
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class Meta:
    model = User
    fields = ('username', 'email', 'password', 'confirm_password')

class Login(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())

    email = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())

    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class Login(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']


from django import forms
from .models import Author, Quote, Tag

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name', )

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('quote', 'author', 'tags')

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', )
