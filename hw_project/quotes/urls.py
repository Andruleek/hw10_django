from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='root'),
    path('login/', views.main, name='login'),
    path('register/', views.register, name='register'),
    path('author/<int:author_id>/', views.main, name='author_profile'),
    path('<int:page>/', views.main, name='root_paginate')
]
