from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from textbook_exchange.models import ProductListing, User, PendingTransaction
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from textexc.settings import EMAIL_HOST_USER
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
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
        if request.user.is_authenticated and "pl_fn_id" in request.COOKIES:
            cart_functions(request.user, request.COOKIES.get("pl_fn_id"), request.COOKIES.get("cart_fn"))
        context=get_cart(request)
        if context['logged_in'] is False:
            return render(request, 'payments/log_in.html')
        context['title'] = "Cart"
        if len(request.user.cart.productlisting_set.all()) == 0:
            return render(request, 'payments/empty_cart.html')
        response = render(request, 'payments/cart.html', context=context)
        if "pl_fn_id" in request.COOKIES:
            response.delete_cookie('pl_fn_id')
            response.delete_cookie("cart_fn")
        return response
    elif request.method == "POST" and request.user.is_authenticated:
        return cart_functions(request.user, request.POST.get("id"), request.POST.get("function"))
    elif request.method == "POST" and not request.user.is_authenticated:
        response = JsonResponse({'status': 'not_logged_in'})
        response.set_cookie("pl_fn_id", request.POST.get("id"))
        response.set_cookie("cart_fn", request.POST.get("function"))
        return response

def one_week_in_future():
    return timezone.now() + timezone.timedelta(weeks=1)

def success(request):
    # TODO: remove items from cart, move to user purchase history
    context=get_cart(request)
    sold_items = []
    for transaction in request.user.cart.productlisting_set.all():
        u = get_object_or_404(User, pk=transaction.user.email)
        pt = PendingTransaction(user=u, balance=transaction.price, date_transacted=timezone.now(), date_settled=one_week_in_future())
        pt.save()
        transaction.has_been_sold = True
        transaction.cart.clear()
        transaction.save()
        transaction.sold_date = datetime.now()
        sold_items.append(transaction)

        subject = 'A textbook sold on UVA TextEx!'
        message = 'Dear ' + transaction.user.first_name +",\n\nYour listing of " + transaction.textbook.title + " has been sold!\n\nIf you have not already been in contact with the buyer, " + request.user.first_name +", make sure you message them or send them an email at " + request.user.email + ". As a reminder, your proceeds from selling the book will be held for two weeks to give the buyer a chance to raise a concern.\n\nThanks for using TextEx for all your used textbook needs,\nThe Team at UVA TextEx"
        recipient = transaction.user.email
        send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)

    context['sold_items'] = sold_items
    
    text_email = get_template('payments/success-email.txt')
    html_email = get_template('payments/success-email.html')

    text_content = text_email.render(context)
    html_content = html_email.render(context)
    send_mail("Your receipt from UVA TextEx", text_content, EMAIL_HOST_USER, [request.user.email], html_message=html_content)


    return render(request, 'payments/success.html', context=context)


def cancelled(request):
    context=get_cart(request)
    return render(request, 'payments/cart.html', context=context)

def cart_functions(user, listing_id, fn):
    listing = get_object_or_404(ProductListing, pk=listing_id)
    if fn == "add":
        listing.cart.add(user.cart)
        listing.save()       
        return JsonResponse({'status': 'success', 'title': listing.textbook.title, 'seller': listing.user.email})
    elif fn == "remove":
        if not user.cart in listing.cart.all():
            return JsonResponse({'status': "error - not authorized to perform this action"})
        listing.cart.remove(user.cart)
        listing.save()
        return JsonResponse({'status': 'success'})