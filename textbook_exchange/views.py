from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import itertools
import functools
import json
import requests
from .forms import SellForm
from .models import ProductListing, Class, Textbook, Class
from django.http import JsonResponse #for autocompletion response
<<<<<<< HEAD
import cloudinary.uploader
import os
=======
from django.conf import settings #for twilio messaging
from faker import Factory #for twilio messaging

from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import (
    SyncGrant,
    ChatGrant
)
>>>>>>> messaging

os.environ["CLOUDINARY_URL"]="cloudinary://348783216512488:nPXIA343WzNVngfkykW-I7XkGgE@dasg2ntne"
cloudinary.config(
  cloud_name = "dasg2ntne", 
  api_key = "348783216512488", 
  api_secret = "nPXIA343WzNVngfkykW-I7XkGgE" 
)

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

def landing(request):
    context=get_logged_in(request)
    return render(request, 'textbook_exchange/landing.html', context=context)

def faq(request):
    context = {}
    context['title'] ='FAQ'
    return render(request, 'textbook_exchange/faq.html', context=context)

def error_404(request):
    context = {}
    context['title'] ='404 Error: Not Found'
    return render(request, 'textbook_exchange/404_error.html')

@login_required(redirect_field_name='my_redirect_field', login_url="/accounts/google/login/")
def sell_books(request):
    context = get_logged_in(request) 
    context['title'] = 'Sell Books'
    context['form'] = SellForm

    submitted = False
    not_logged_in = False
    if request.method == 'POST':
        if not context['logged_in']:
            form = SellForm()
            return HttpResponseRedirect('/sell?not_logged_in=True')
        elif context['logged_in']:
            form = SellForm(request.POST, request.FILES)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user = request.user

                listing_obj = ProductListing()
                listing_obj.user = user
                listing_obj.price = cleaned_data['price']
                listing_obj.condition = cleaned_data['book_condition']
                response = cloudinary.uploader.upload(cleaned_data['picture'])
                listing_obj.picture_url = response['url']
                listing_obj.comments = cleaned_data['comments']
                
                # finding textbook using isbn
                isbn = cleaned_data['isbn']
                txtbk = get_object_or_404(Textbook, isbn13=isbn) # takes in bookstore_isbn
                listing_obj.textbook = txtbk
                
                listing_obj.save()
                return HttpResponseRedirect('/sell?submitted=True')
            else:
                return render(request, "textbook_exchange/sellbooks.html", context={'form':form})
                # raise forms.ValidationError("Please fill in all fields in red.")

    else:
        if 'submitted' in request.GET:
            context['submitted'] = True
        if 'not_logged_in' in request.GET:
            context['not_logged_in'] = True

    return render(request, 'textbook_exchange/sellbooks.html', context=context)

def account_page(request):
    context = get_logged_in(request)
    context['title'] = 'Account Page'
    if not context['logged_in']:
        return HttpResponseRedirect('/404_error')    
    return render(request, 'textbook_exchange/account_dashboard.html', context=context)

def account_page_messages(request):
    context = get_logged_in(request)
    context['title'] = 'Messages'
    if not context['logged_in']:
        return HttpResponseRedirect('/404_error')    
    return render(request, 'textbook_exchange/account_messages.html', context=context)

def account_page_past_posts(request):
    context = get_logged_in(request)
    context['title'] = 'Past Posts'
    if not context['logged_in']:
        return HttpResponseRedirect('/404_error')
    return render(request, 'textbook_exchange/account_current_posts.html', context=context)

class AccountCurrentListings(ListView):
    model = ProductListing
    template_name = "textbook_exchange/account_dashboard.html"
    context_object_name = 'current_posts'
    ordering = ['published_date']

class AccountPastListings(ListView):
    model = ProductListing
    template_name = "textbook_exchange/account_past_posts.html"
    context_object_name = 'past_posts'
    ordering = ['published_date']

    def get_queryset(self):
        queryset = super(AccountPastListings, self).get_queryset()
        queryset = queryset.filter(user=self.request.user, hasBeenSoldFlag=True)
        return queryset

def buy_books(request):    
    context = get_logged_in(request)
    context['title'] ='Buy Books'
    if request.GET.get("search"):
        context['search'] = request.GET.get('search')
    return render(request, 'textbook_exchange/buybooks.html', context=context)

class BuyProductListings(ListView):
    model = ProductListing
    template_name = "textbook_exchange/buybooks.html"
    context_object_name = 'product_listings'
    
    def get_context_data(self, **kwargs):
        url_ibsn = self.kwargs['isbn']
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['slug']
        context['textbook'] = get_object_or_404(Textbook, isbn13=url_ibsn)
        context['num_product_listings'] = len(get_object_or_404(Textbook, isbn13=url_ibsn).productlisting_set.all())
        
        context['ordering'] = self.request.GET.get('sort')
        if context['ordering'] == "-price":
            context['ordering'] = "Price High to Low"
        elif context['ordering'] == "-published_date":
            context['ordering'] = "Most Recent"
        else:
            context['ordering'] = "Price Low to High"

        return context

    def get_queryset(self, *args, **kwargs):
        url_ibsn = self.kwargs['isbn']
        url_ordering = self.request.GET.get('sort')

        textbook = get_object_or_404(Textbook, isbn13=url_ibsn)
        product_listings = textbook.productlisting_set.all()
        queryset = product_listings.filter(hasBeenSoldFlag=False, cart=None)

        if url_ordering is not None:
            queryset = queryset.order_by(url_ordering)
        else:
            queryset = queryset.order_by('price')
            
        return queryset

class FindTextbooks(ListView):
    model = Textbook
    template_name = "textbook_exchange/find_by_class.html"
    context_object_name = 'textbooks'
    
    def get_context_data(self, **kwargs):
        url_class_info = self.kwargs['class_info']
        context = super().get_context_data(**kwargs)
        context['class'] = get_object_or_404(Class, class_info=url_class_info)
        context['num_textbooks'] = len(get_object_or_404(Class, class_info=url_class_info).textbook_set.all())

        return context

    def get_queryset(self, *args, **kwargs):
        url_class_info = self.kwargs['class_info']
        class_found = get_object_or_404(Class, class_info=url_class_info)
        textbooks = class_found.textbook_set.all()
        queryset = textbooks            
        return queryset


def autocomplete(request):
    search = request.GET['search']

    #these will search in our models for matches
    b_starts_with = Textbook.objects.filter(title__istartswith=search) # first we want searches that start with the search term, then we want everything else
    books = Textbook.objects.filter(title__icontains=search) | Textbook.objects.filter(author__icontains=search) | Textbook.objects.filter(isbn13__icontains=search) | Textbook.objects.filter(isbn10__icontains=search) | Textbook.objects.filter(bookstore_isbn__icontains=search) # TODO: Add other methods to search
    courses = Class.objects.filter(class_info__icontains=search.replace(" ", "")) | Class.objects.filter(class_title__icontains=search)
    
    valid_books = []
    valid_courses = []

    # add books that start with the search query first, up to a max of 6 books
    # we only display up to 6 search items, so dont send more than we can view, thats a waste of data
    for book in list(b_starts_with.order_by("title", 'isbn13')):
        if len(valid_books) >= 6:
            break
        valid_books.append(book.toJSON())

    # if we need more books than just ones that start with the query, we first need to filter out any books that have already been added to the return list
    if len(valid_books) < 6:
            books = books.difference(b_starts_with)

    for book in list(books.order_by("title", 'isbn13')):
        if len(valid_books) >= 6:
            break
        valid_books.append(book.toJSON())

    for course in list(courses.order_by("class_title")):
        if len(valid_courses) >= 6:
            break
        valid_courses.append(course.toJSON())
        
    data = {
        'search' : search,
        'books' : valid_books,
        'courses' : valid_courses,
    }

    return JsonResponse(data)

def chat_view(request):
    return render(request, 'textbook_exchange/index.html')
    
def token(request):
    fake = Factory.create()
    return generateToken(fake.user_name())

def generateToken(identity):
    # Get credentials from environment variables
    account_sid      = settings.TWILIO_ACCT_SID
    chat_service_sid = settings.TWILIO_CHAT_SID
    sync_service_sid = settings.TWILIO_SYNC_SID
    api_sid          = settings.TWILIO_API_SID
    api_secret       = settings.TWILIO_API_SECRET

    # Create access token with credentials
    token = AccessToken(account_sid, api_sid, api_secret, identity=identity)

    # Create a Sync grant and add to token
    if sync_service_sid:
        sync_grant = SyncGrant(service_sid=sync_service_sid)
        token.add_grant(sync_grant)

    # Create a Chat grant and add to token
    if chat_service_sid:
        chat_grant = ChatGrant(service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    # Return token info as JSON
    return JsonResponse({'identity':identity,'token':token.to_jwt().decode('utf-8')})
