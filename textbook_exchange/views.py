from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django import forms

from .forms import SellForm
from .models import ProductListing

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


# Followed this tutorials: https://djangobook.com/mdj2-django-forms/
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

            # TODO: validate the ISBN and throw error if not valid

            listing_obj = ProductListing() #gets new object
            # listing_obj.textbook.title = cleaned_data['book_title']
            # listing_obj.textbook.author = cleaned_data['book_author']
            # listing_obj.textbook.isbn = cleaned_data['isbn']
            listing_obj.condition = cleaned_data['book_condition']
            listing_obj.price = cleaned_data['price']
            listing_obj.picture = cleaned_data['picture']
            listing_obj.comments = cleaned_data['comments']

            # TODO: find this book in UVA books and save with that foreign key
            # user=request.user
            # https://stackoverflow.com/questions/24793385/django-saving-form-with-user-as-foreign-key
            
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
