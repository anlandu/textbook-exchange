from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('buy/', views.buy_books, name='buybooks'),
]