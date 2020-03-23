from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "payments"

urlpatterns = [
    path('complete/', views.complete, name='confirm'),
    path('return/', views.redirect, name='redirect')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
