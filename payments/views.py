from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from textbook_exchange import models as textbook_exchange_models
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import requests, json

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
    if request.method == "GET":
        context=get_cart(request)
        if context['logged_in'] is False:
            return render(request, 'payments/log_in.html')
        context['title'] = "Cart"
        if len(request.user.cart.productlisting_set.all()) == 0:
            return render(request, 'payments/empty_cart.html')
        return render(request, 'payments/cart.html', context=context)
    elif request.method == "POST" and request.user.is_authenticated:
        listing = textbook_exchange_models.ProductListing.objects.get(pk=request.POST.get("id"))
        if request.POST.get("function") == "add":
            listing.cart = request.user.cart
            listing.save()       
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')

        elif request.POST.get("function") == "remove":
            listing.cart = None
            listing.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')

        return HttpResponse(json.dumps({'status': 'error'}), content_type='application/json')


    elif request.method == "POST" and not request.user.is_authenticated:
        return HttpResponse(json.dumps({'status': 'not_logged_in'}), content_type='application/json')

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
