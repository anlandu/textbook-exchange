from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from textbook_exchange import models as textbook_exchange_models
import requests

def get_cart(request):
    if request.user.is_authenticated:
        subtotal = 0
        for pl in request.user.cart.productlisting_set.all():
            subtotal += pl.price

        context = {
            'logged_in': True,
            'subtotal': subtotal,
            'currency': 'USD',
            'cart': request.user.cart
        }
    else:
        context = {
            'logged_in': False,
        }
    return context

def cart(request):
    context=get_cart(request)
    if context['logged_in'] is False:
        return render(request, 'payments/log_in.html')
    else:
        return render(request, 'payments/cart.html', context=context)

def success(request):
    # TODO: remove items from cart, mark them as sold and move to user purchase history
    context=get_cart(request)
    return render(request, 'payments/success.html', context=context)

def cancelled(request):
    context=get_cart(request)
    return render(request, 'payments/cart.html', context=context)