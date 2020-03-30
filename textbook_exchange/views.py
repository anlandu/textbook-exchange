from django import forms
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import ListView
from django.contrib import messages
import itertools
import functools

from .forms import SellForm
from .models import ProductListing, Class, Textbook, Class
from django.http import JsonResponse #for autocompletion response


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
        context['search'] = request.GET.get('search')
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

def autocomplete(request):
    search = request.GET['search']

    #these will search in our models for matches
    books = Textbook.objects.filter(title__icontains=search) | Textbook.objects.filter(author__icontains=search) | Textbook.objects.filter(isbn13__icontains=search) | Textbook.objects.filter(isbn10__icontains=search) | Textbook.objects.filter(bookstore_isbn__icontains=search) # TODO: Add other methods to search
    courses = Class.objects.filter(course_code__icontains=search.replace(" ", ""))
    
    valid_books = []
    valid_courses = []

    for book in list(books):
        valid_books.append(book.toJSON())

    for course in list(courses):
        valid_courses.append(course.toJSON())

    data = {
        'search' : search,
        'books' : valid_books,
        'courses' : valid_courses,
    }

    return JsonResponse(data)
