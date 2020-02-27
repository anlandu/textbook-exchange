from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django import forms

from .forms import SellForm
from .models import Listing

def get_logged_in(request):
    if request.user.is_authenticated:
        context = {
            'logged_in': True,
        }
    else:
        context = {
            'logged_in': False,
        }
    return context

# Create your views here.
def landing(request):
    context=get_logged_in(request)

    return render(request, 'textbook_exchange/landing.html', context=context)

def buy_books(request):
    context=get_logged_in(request)
    context['title'] ='Buy Books'

    return render(request, 'textbook_exchange/buybooks.html', context=context)


# https://djangobook.com/mdj2-django-forms/
def sell_books(request):
    # context=get_logged_in(request)
    # context['title'] ='Sell Books'
    # context['form'] = SellForm
    submitted = False
    if request.method == 'POST':
        form = SellForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # assert False

            listing_obj = Listing() #gets new object
            listing_obj.business_name = cleaned_data['business_name']
            listing_obj.business_email = cleaned_data['business_email']
            listing_obj.business_phone = cleaned_data['business_phone']
            listing_obj.business_website = cleaned_data['business_website']

            listing_obj.save()

            return HttpResponseRedirect('/sell_books?submitted=True')
    else:
        form = SellForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'textbook_exchange/sellbooks.html', {'form': form, 'submitted': submitted})

def account_page(request):
    context = get_logged_in(request)
    context['title'] = 'Account Page'

    #save if you mde chnges to dtbse

    return render(request, 'textbook_exchange/account_page.html', context=context)
