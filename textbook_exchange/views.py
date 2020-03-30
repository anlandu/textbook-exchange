from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import itertools
import functools

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

def error_404(request):
    return render(request, 'textbook_exchange/404_error.html')

def buy_books(request):    
    context = get_logged_in(request)
    context['title'] ='Buy Books'
    if (request.GET.get("search")):
        context['search'] = request.GET.get('search');
    return render(request, 'textbook_exchange/buybooks.html', context=context)


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
                listing_obj.picture = cleaned_data['picture']
                listing_obj.comments = cleaned_data['comments']
                
                # finding textbook using isbn
                isbn = cleaned_data['isbn']
                txtbk = Textbook.objects.get(pk=isbn)
                listing_obj.textbook = txtbk
                
                listing_obj.save()

                return HttpResponseRedirect('/sell?submitted=True')
            else:
                print(form.errors)
                # raise forms.ValidationError("Please fill in all fields in red.")

    else:
        form = SellForm()
        if 'submitted' in request.GET:
            submitted = True
        if 'not_logged_in' in request.GET:
            not_logged_in = True

    return render(request, 'textbook_exchange/sellbooks.html', {'form': form, 'submitted': submitted, 'not_logged_in': not_logged_in})

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
    ordering = ['-published_date']

    def get_queryset(self):
        queryset = super(AccountCurrentListings, self).get_queryset()
        queryset = queryset.filter(user=self.request.user, hasBeenSoldFlag=False)
        return queryset

class AccountPastListings(ListView):
    model = ProductListing
    template_name = "textbook_exchange/account_past_posts.html"
    context_object_name = 'past_posts'
    ordering = ['-published_date']

    def get_queryset(self):
        queryset = super(AccountPastListings, self).get_queryset()
        queryset = queryset.filter(user=self.request.user, hasBeenSoldFlag=True)
        return queryset

class BuyProductListings(ListView):
    model = ProductListing
    template_name = "textbook_exchange/buybooks.html"
    context_object_name = 'product_listings'
    ordering = ['price']
    
    def get_context_data(self, **kwargs):
        url_ibsn = self.kwargs['isbn']

        context = super().get_context_data(**kwargs)
        context['textbook'] = Textbook.objects.get(isbn=url_ibsn)
        context['num_textbooks'] = len(Textbook.objects.filter(isbn=url_ibsn))
        context['num_product_listings'] = Textbook.objects.get(isbn=url_ibsn).productlisting_set.all().count()
        
        return context

    def get_queryset(self, *args, **kwargs):
        url_ibsn = self.kwargs['isbn']
        textbook = Textbook.objects.get(isbn=url_ibsn)
        product_listings = textbook.productlisting_set.all()
        queryset = product_listings.filter(hasBeenSoldFlag=False)
        return queryset

    # def get_queryset(self):
    #     try: # textbook exists
    #         textbook = Textbook.objects.get(isbn=self.kwargs['isbn'])
    #         product_listings = textbook.productlisting_set.all()
    #         queryset = product_listings.filter(hasBeenSoldFlag=False)
    #         return queryset
    #     except ObjectDoesNotExist: # textbook doesn't exist (invalid ibsn)
    #         # display error msg on buybooks.html

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
