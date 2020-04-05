from django.urls import path
from . import views
from . import forms
# from django.contrib import admin
# from django.urls import include, path
# from django.contrib.auth import views as auth_views

app_name = "exchange"

urlpatterns = [
    path('', views.landing, name='landing'),
    path('buy/', views.buy_books, name='buybooks'),
    path('sell/', views.sell_books, name='sellbooks'),
    path('accounts/', views.account_page, name='account_page'),
    path('buy/autocomplete/', views.autocomplete, name='ajax_autocomplete'),
    path('messaging/', views.chat_view, name='twilio'),
    path(r'^token', views.token, name='token'),
]
