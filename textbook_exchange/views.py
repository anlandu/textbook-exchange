from django import forms
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import ListView
from django.contrib import messages


from .forms import SellForm
from .models import ProductListing, Class, Textbook
from django.http import JsonResponse #for autocompletion response

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

def landing(request):
    context=get_logged_in(request)

    return render(request, 'textbook_exchange/landing.html', context=context)

def buy_books(request):    
    context = get_logged_in(request)
    context['title'] ='Buy Books'
    if (request.GET.get("search")):
        context['search'] = request.GET.get('search');
    return render(request, 'textbook_exchange/buybooks.html', context=context)


def sell_books(request):
    context = get_logged_in(request) 
    context['title'] = 'Sell Books'
    # context['form'] = SellForm

    submitted = False
    not_logged_in = False
    if request.method == 'POST':
        if not context['logged_in']:
            form = SellForm()
            # return render(request, 'textbook_exchange/sellbooks.html', {'not_logged_in': True}) 
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
                listing_obj.picture = cleaned_data['picture']
                listing_obj.comments = cleaned_data['comments']
                listing_obj.published_date = timezone.now()
                listing_obj.hasBeenSoldFlag = False

                isbn = cleaned_data['isbn']
                txtbk = Textbook.objects.get(pk=isbn)
                listing_obj.textbook = txtbk
                
                # TODO: find class codes from dtbse (query) + split + add to class_object
                # class_codes = .split(" ")
                # for class in class_codes:
                #       listing_obj.class_object.add(class)
                
                listing_obj.save()

                return HttpResponseRedirect('/sell?submitted=True')
            else:
                print(form.errors)
    else:
        form = SellForm()
        if 'submitted' in request.GET:
            submitted = True
        if 'not_logged_in' in request.GET:
            not_logged_in = True

    return render(request, 'textbook_exchange/sellbooks.html', {'form': form, 'submitted': submitted, 'not_logged_in': not_logged_in})

class ProductListingListView(ListView):
    model = ProductListing
    template_name = "textbook_exchange/account_page.html"
    context_object_name = 'current_posts' #var being passed in
    ordering = ['-dateposted']
    # queryset = ProductListing.objects.filter(user=self.request.user) #test


def account_page(request):
    context = get_logged_in(request)
    context['title'] = 'Account Page'

    return render(request, 'textbook_exchange/account_page.html', context=context)

def autocomplete(request):
    search = request.GET['search']

    #normalize search -- we'll add more as we understand our data better
    search = search.lower() 
    
    #these will search in our models for matches
    books = textbook_exchange_models.Textbook.objects.filter(
        isbn__contains = search, title__contains = search, author__contains = search)
    courses = textbook_exchange_models.Class.objects.filter(course_code__contains = search.replace(" ", ""))
    
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
