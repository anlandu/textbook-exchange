from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from textbook_exchange import models as textbook_exchange_models
import requests

def get_cart(request):
    if request.user.is_authenticated:
        context = {
            'logged_in': True,
            'subtotal': 123.45,
            'currency': 'USD',
        }
    else:
        context = {
            'logged_in': False,
        }
    return context

def get_paypal_access_token(request):
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
    }
    r = requests.post(url, headers=headers, auth=("AcCaARG0gidap3Y0mCgZtbbdE3sDrYHyHSIBwJ20jwhyGk3MQSBLxpWggOwuOQphYKDLl87wRLek-qE8", "ENBevuGci9BP5Lt7bAfofOFvjVerx7hMHKaapIo0-8idONUuQkx90pyyKM7HHAIlMYirX5mDRoc_zPFI"), data="grant_type=client_credentials")
    return r.json()['access_token']

def complete(request):
    context=get_cart(request)
    if context['logged_in'] is False:
        return HttpResponseRedirect('/')
    else:
        return render(request, 'payments/cart.html', context=context)

def redirect(request):
    context=get_cart(request)

    return render(request, 'textbook_exchange/landing.html', context=context)
