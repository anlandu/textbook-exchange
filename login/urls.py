from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from login.views import OAuth, OAuth2CallBack, TempHome, TempLogout

app_name="login"

urlpatterns = [
    url('oauth/$', csrf_exempt(OAuth.as_view()), name='oauth'),
    url('oauth2callback/$', OAuth2CallBack.as_view(), name='oauth2_callback'),
    path('', TempHome.as_view(), name='home'),
    path('logout/', TempLogout.as_view(), name='logout')
]
