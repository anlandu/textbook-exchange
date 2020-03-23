from django.urls import path
from . import views
from . import forms
from .views import AccountCurrentListings, AccountPastListings
# from django.contrib import admin
# from django.urls import include, path
# from django.contrib.auth import views as auth_views

app_name = "exchange"

urlpatterns = [
    path('', views.landing, name='landing'),
    path('404_error', views.error_404, name='404_error'),
    path('buy/', views.buy_books, name='buybooks'),
    path('sell/', views.sell_books, name='sellbooks'),
    path('accounts/', views.account_page, name='account_page'),
    path('accounts/current_posts', views.AccountCurrentListings.as_view(), name='account_page_current_posts'),
    path('accounts/past_posts', views.AccountPastListings.as_view(), name='account_page_past_posts'),
    path('buy/autocomplete/', views.autocomplete, name='ajax_autocomplete'),
]
