from django.urls import path
from . import views

app_name = "exchange"

urlpatterns = [
    path('', views.landing, name='landing'),
    path('buy/', views.buy_books, name='buybooks'),
    path('sell/', views.sell_books, name='sellbooks')
]