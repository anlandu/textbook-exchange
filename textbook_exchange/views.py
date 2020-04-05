from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django import forms
from django.utils import timezone

from .forms import SellForm
from .models import ProductListing
from django.http import JsonResponse #for autocompletion response
from django.conf import settings #for twilio messaging
from faker import Factory #for twilio messaging

from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import (
    SyncGrant,
    ChatGrant
)

from textbook_exchange import models as textbook_exchange_models

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
    if (request.GET.get("search")):
        context['search'] = request.GET.get('search');
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
            # listing_obj.textbook.title = cleaned_data['book_title']
            # listing_obj.textbook.author = cleaned_data['book_author']
            # listing_obj.textbook.isbn = cleaned_data['isbn']
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

def autocomplete(request):
    search = request.GET['search']

    #normalize search -- we'll add more as we understand our data better
    search = search.lower() 
    
    #these will search in our models for matches
    books = textbook_exchange_models.Textbook.objects.filter(
        isbn__contains = search, title__contains = search, author__contains = search)
    courses = textbook_exchange_models.Class.objects.filter(class_code__contains = search.replace(" ", ""))
    
    #using fake data for demo
    some_courses = ['CS1110', 'CS2110', 'CS2102', 'CS2150','CS2330',
    'CS3102', 'CS3330','APMA1110','APMA2120','APMA3100','CHEM160',
    'ENGR1620','PHYS1425','PHYS2415','ECON2010','ECON2020','ECON3010',
    'HIUS2060','HIUS2051', 'COMM2010', 'STS1500', 'STS2500']

    some_books = [
    {'isbn' : "1234567890123", 'author' : "Zane Alpher", 'title' : "Intro to CS", 'class_key' : "CS1110"},
    {'isbn' : "5435678966577", 'author' : "Nick Winans", 'title' : "Object Oriented Programming",  'class_key' : "CS2110"},
    {'isbn' : "8765434512356", 'author' : "Rohan Chandra", 'title' : "American Economic History", 'class_key' : "HIUS2060"},
    {'isbn' : "2345673452898", 'author' : "Anlan Du", 'title' : "Physics for Engineers", 'class_key' : "PHYS2415"},
    {'isbn' : "0318975198234", 'author' : "Zaeda Meherin", 'title' : "Intro to Microeconomics", 'class_key' : "ECON2010"},
    {'isbn' : "7283916493821", 'author' : "Mark Sherriff", 'title' : "Software Engineering", 'class_key' : "CS3240"},
    ]

    matched_classes = list(filter(lambda x: search in x.lower(), some_courses))
    matched_books = list(filter(lambda x: search in x['isbn'] or search in x['author'].lower() or search in x['title'].lower(), some_books))

    data = {
        'search' : search,
        'books' : matched_books,
        'courses' : matched_classes,
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
