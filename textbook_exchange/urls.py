from django.urls import path
from . import views
from . import forms
from .views import CurrentListings
# from django.contrib import admin
# from django.urls import include, path
# from django.contrib.auth import views as auth_views

app_name = "exchange"

urlpatterns = [
    path('', views.landing, name='landing'),
    path('404_error', views.error_404, name='404_error'),
    path('buy/', views.buy_books, name='buybooks'),
    path('sell/', views.sell_books, name='sellbooks'),
    path('accounts/', views.CurrentListings.as_view(), name='account_page'),
    path('buy/autocomplete/', views.autocomplete, name='ajax_autocomplete'),
]
