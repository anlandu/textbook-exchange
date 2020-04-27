from django.urls import path
from . import views
from . import forms
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
# from django.contrib import admin
# from django.urls import include, path
# from django.contrib.auth import views as auth_views

app_name = "exchange"

urlpatterns = [
    path('', views.landing, name='landing'),
    path('faq', views.faq, name='faq'),
    path('login/', views.login_redirect_before, name="login"),
    path('login/redirect/', views.login_redirect_after, name="login_redirect"),
    path('sell/', views.sell_books, name='sellbooks'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('accounts/', login_required(views.AccountCurrentListings.as_view(), redirect_field_name='login_redirect_target', login_url="/login/"), name='account_page'),
    path('accounts/edit/<int:listing_id>/<slug:title>', views.edit_post, name='edit_post'),
    path('accounts/past_posts', login_required(views.AccountPastListings.as_view(), redirect_field_name='login_redirect_target', login_url="/login/"), name='past_posts'),
    path('accounts/messages', views.account_page_messages, name='messages'),
    path('accounts/cashout', views.cashout, name='cashout'),
    path('accounts/process', views.process_pending, name='process'),
    path('buy/', views.buy_books, name='buybooks'),
    path('search/<slug:keywords>/', views.SearchTextbooks.as_view(), name='search'),
    path('buy/autocomplete/', views.autocomplete, name='ajax_autocomplete'),
    path('buy/<slug:isbn>/<slug:slug>/', views.BuyProductListings.as_view(), name='buy_product'), 
    path('buy/<slug:isbn>/<slug:slug>/<slug:sort>/', views.BuyProductListings.as_view(), name='buy_product'), 
    path('find/<slug:class_info>/', views.FindTextbooks.as_view(), name='find_by_class'), 
    path('messaging/', views.chat_view, name='twilio'),
    path('token/', views.token, name='token'),
    path('messaging/channel', views.channel_view, name='channel'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
