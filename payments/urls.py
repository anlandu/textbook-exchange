from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path('complete/', views.complete, name='confirm'),
    path('return/', views.redirect, name='redirect')
]
