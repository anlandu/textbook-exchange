from django.urls import path
from . import views
from . import forms
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import include, path
# from django.contrib.auth import views as auth_views

app_name = "exchange"

urlpatterns = [
    path('', views.landing, name='landing'),
    path('404_error', views.error_404, name='404_error'),
    path('sell/', views.sell_books, name='sellbooks'),
    path('accounts/', views.AccountCurrentListings.as_view(), name='account_page'),
    path('accounts/past_posts', views.AccountPastListings.as_view(), name='past_posts'),
    path('accounts/messages', views.account_page_messages, name='messages'),
    path('buy/', views.buy_books, name='buybooks'),
    path('buy/autocomplete/', views.autocomplete, name='ajax_autocomplete'),
    path('buy/<slug:isbn>/', views.BuyProductListings.as_view(), name='buy_product'), 
    path('buy/<slug:isbn>/<slug:slug>/', views.BuyProductListings.as_view(), name='buy_product'), 
    path('buy/<slug:isbn>/<slug:slug>/<slug:sort>/', views.BuyProductListings.as_view(), name='buy_product'), 

    # https://stackoverflow.com/questions/14351048/django-optional-url-parameters
    # path('buy/<slug:isbn>/<int:maxprice>/', views.BuyProductListings.as_view(), name='buy_product'),
    # url(r'^list$', views.product_list),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)