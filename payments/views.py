from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from textbook_exchange import models as textbook_exchange_models
from django.utils import timezone
import requests

def get_cart(request):        
    if request.user.is_authenticated:
        subtotal = 0
        for pl in request.user.cart.productlisting_set.all():
            subtotal += pl.price
        tax = round(5 * subtotal)/100
        total = round(105 * subtotal)/100
        context = {
            'logged_in': True,
            'subtotal': subtotal,
            'tax': tax,
            'total': total,
            'currency': 'USD',
        }
    else:
        context = {
            'logged_in': False,
        }
    return context

def cart(request):
    context=get_cart(request)
    if request.method == "GET":
        if len(request.user.cart.productlisting_set.all()) == 0:
            return render(request, 'payments/empty_cart.html')
        if context['logged_in'] is False:
            return render(request, 'payments/log_in.html')
        else:
            return render(request, 'payments/cart.html', context=context)
    elif request.method == "POST":
        if context['logged_in'] is False:
            return HttpResponse("failed")
        listing = textbook_exchange_models.ProductListing.objects.get(pk=request.POST.get("id"))
        listing.cart = request.user.cart
        listing.save()
        return HttpResponse("success")

def one_week_in_future():
    return timezone.now() + timezone.timedelta(weeks=1)

def success(request):
    # TODO: remove items from cart, mark them as sold and move to user purchase history
    context=get_cart(request)
    for transaction in request.user.cart.productlisting_set.all():
        u = textbook_exchange_models.User.objects.get(pk=transaction.user.email)
        pt = textbook_exchange_models.PendingTransaction(user=u, balance=transaction.price, date_transacted=timezone.now(), date_settled=one_week_in_future())
        pt.save()
        transaction.hasBeenSoldFlag = True
        transaction.cart = None
        transaction.save()
    return render(request, 'payments/success.html', context=context)

def cancelled(request):
    context=get_cart(request)
    return render(request, 'payments/cart.html', context=context)