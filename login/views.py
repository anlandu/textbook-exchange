from django.shortcuts import render
from google_auth_oauthlib.flow import Flow
from django.conf import settings
from oauth2client.client import OAuth2WebServerFlow
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed, HttpResponse
import httplib2
import json
from django.urls import reverse
from django.views import generic

class BuildFlow:
    def __init__(self):
        self.flow = OAuth2WebServerFlow(
            settings.CLIENT_ID,
            settings.CLIENT_SECRET,
            scope=['email'],
            redirect_uri=settings.REDIRECT_URI)

class OAuth(generic.View):
    def get(self, request, *args, **kwargs):
        build_flow = BuildFlow()
        generated_url = build_flow.flow.step1_get_authorize_url()
        return HttpResponseRedirect(generated_url)

class OAuth2CallBack(generic.View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', False)
        if not code:
            return JsonResponse({'status': 'error, no access key received from Google or User declined permission!'})
        domain = request.GET.get('hd', False)
        #if domain != "virginia.edu":
         #   return JsonResponse({'status': "You must login with your UVA email account to verify your status as a UVA student!"})
        
        oauth2 = BuildFlow()
        credentials = oauth2.flow.step2_exchange(code)

        http = httplib2.Http()
        http = credentials.authorize(http)

        credentials_js = json.loads(credentials.to_json())
        access_token = credentials_js['access_token']
        email = credentials_js['id_token']['email']
        if 'hd' in credentials_js['id_token']:
            domain = credentials_js['id_token']['hd']
        else:
            domain = "gmail"

        #if domain != "virginia.edu":
        #    return HttpResponse("Please log in with your UVA email address. This is so we can verify every student is from UVA!<br><a href='logout'>Logout?</a>")

        request.session['access_token'] = access_token
        request.session['current_email'] = email
        request.session['email_domain'] = domain

        return HttpResponseRedirect(reverse('login:home'))

    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Only GET requests!')

class TempHome(generic.View):
    def get(self, request, *args, **kwargs):
        if 'access_token' in request.session:
            if request.session['access_token'] != "":
                if request.session['email_domain'] != "virginia.edu":
                    return HttpResponse("Please log in with your UVA email address. This is so we can verify every student is from UVA!<br><a href='logout'>Logout?</a>")
                return HttpResponse('Welcome ' + request.session['current_email'] + "!" + '<br><a href="logout">Logout?</a>')
        return HttpResponse("You're not logged in! Would you like to <a href='oauth'>log in?</a>")

class TempLogout(generic.View):
    def get(self, request, *args, **kwargs):
        request.session['access_token'] = ""
        request.session['current_email'] = ""
        request.session['email_domain'] = ""
        return HttpResponseRedirect(reverse('login:home'))
