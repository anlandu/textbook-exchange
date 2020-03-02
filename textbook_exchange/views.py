from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django import forms
from django.utils import timezone

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
        form = SellForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # assert False

            # TODO: validate the ISBN and throw error if not valid

            listing_obj = ProductListing() #gets new object
            listing_obj.condition = cleaned_data['book_condition']
            listing_obj.price = cleaned_data['price']
            listing_obj.picture = cleaned_data['picture']
            listing_obj.comments = cleaned_data['comments']
            listing_obj.published_date = timezone.now()
            listing_obj.class_object_id = 3240 
            listing_obj.textbook_id = 111
            listing_obj.user_id = 'nw5zp@virginia.edu'

            # TODO: find this book in UVA books and save with that foreign key
            # user=request.user
            
            # listing_obj.textbook.isbn = cleaned_data['isbn']
            # Query dtbse for tht ISBN (or title) for listing_obj.textbook.isbn (this isbn finds the rest of title, author, isbn)
            # find that query
            # listing_obj.textbook = query

            # listing_obj.user = user #(user pk)?

            # https://stackoverflow.com/questions/24793385/django-saving-form-with-user-as-foreign-key
            
            listing_obj.save()

            return HttpResponseRedirect('/sell?submitted=True')
        else:
            print(form.errors)
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
