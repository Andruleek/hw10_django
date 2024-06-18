from django.shortcuts import render, redirect
from .utils import get_mongodb
from django.core.paginator import Paginator
from bson.objectid import ObjectId
from .models import Quote, Tag, Author
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import AuthorForm, QuoteForm, TagForm

# Create your views here.

def main(request, page=1):
    db = get_mongodb()
    quotes = list(db.quotes.find())
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})

def author_about(request, author_id):
    db = get_mongodb()
    author = db.authors.find_one({'_id': ObjectId(author_id)})
    return render(request, 'quotes/author.html', context={'author': author})

def tag_page(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    quotes_with_tag = Quote.objects.filter(tags=tag)
    return render(request, 'quotes/tag.html', {'quotes_with_tag': quotes_with_tag, 'tag': tag})

def author_for_tag(request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, 'quotes/author_for_tag.html', context={'author': author})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_author.html', context={'form': form})
    return render(request, 'quotes/add_author.html', context={'form': AuthorForm()})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()
            tag_name = form.cleaned_data["tags"]
            for tag in tag_name:
                new_quote.tags.add(tag.id)
            new_quote.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_quote.html', context={'form': form})
    return render(request, 'quotes/add_quote.html', context={'form': QuoteForm()})

@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_tag.html', context={'form': form})
    return render(request, 'quotes/add_tag.html', context={'form': TagForm()})

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetConfirmView

class Login(LoginView):
    template_name = 'quotes/login.html'
    authentication_form = AuthenticationForm

def custom_password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, 'Password reset email sent successfully.')
            return redirect('users:login')
    else:
        form = PasswordResetForm()
    return render(request, 'quotes/password_reset.html', {'form': form})

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'quotes/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')

def custom_password_reset_done_view(request):
    messages.success(request, 'Password reset successful. Please log in.')
    return redirect('users:login')

custom_login = Login.as_view()
custom_password_reset = custom_password_reset_view
custom_password_reset_confirm = CustomPasswordResetConfirmView.as_view()
custom_password_reset_done = custom_password_reset_done_view

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'quotes/signup.html'
    success_url = reverse_lazy('quotes:login')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)