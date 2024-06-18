from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='root'),  
    path('<int:page>', views.main, name='root_paginate'),
    path('author/<str:author_id>', views.author_about, name='author_about'),
    path('tag/<str:tag_name>/', views.tag_page, name='tag_page'),
    path('author_for_tag/<int:author_id>', views.author_for_tag, name='author_for_tag'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='Login'),
    path('logout/', views.logout, name='Logout'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url='/users/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
   ]

