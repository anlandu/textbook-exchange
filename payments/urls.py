from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "payments"

urlpatterns = [
    path('', views.cart, name='cart'),
    path('checkout/success/', views.success, name='success'),
    path('checkout/cancelled/', views.cancelled, name='cancelled')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
