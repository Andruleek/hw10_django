from django.core.paginator import Paginator
from django.shortcuts import render
from .utils import get_mongodb
from .models import Author
from django.db.models import Q


# Create your views here.

def main(request, page=1):
    db = get_mongodb()
    quotes = list(db.quotes.find())
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'quotes/register.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'quotes/register.html', {'form': form})