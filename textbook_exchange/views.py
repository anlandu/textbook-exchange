from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django import forms

from .forms import SellForm

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

# def sell_books(request):
#     context=get_logged_in(request)
#     context['title'] ='Sell Books'
#     context['form'] = SellForm
    
#     return render(request, 'textbook_exchange/sellbooks.html', context=context)

def sell_on_submit(request):
    submitted = False
    if request.method == 'POST':
        form = SellForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            assert False
            return HttpResponseRedirect('/sell_on_submit?submitted=True')
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
