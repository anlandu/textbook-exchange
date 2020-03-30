from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
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

        # url_maxprice = self.kwargs['maxprice']
        # url_likenew = self.kwargs['likenew']
        # url_verygood = self.kwargs['verygood']
        # url_good = self.kwargs['good']
        # url_acceptable = self.kwargs['acceptable']

        url_maxprice = self.request.GET.get("maxprice")
        url_likenew = self.request.GET.get('likenew')
        url_verygood = self.request.GET.get('verygood')
        url_good = self.request.GET.get('good')
        url_acceptable = self.request.GET.get('acceptable')

        # add filters
        if url_maxprice is not None and url_maxprice > 0:
            queryset.filter(price__lte=url_maxprice)
            print("mxprice")
        if url_likenew is not None and not url_likenew:
            queryset.exclude(condition="likenew")
            print("likenew")
        if url_verygood is not None and not url_verygood:
            queryset.exclude(condition="verygood")
            print("vgood")
        if url_good is not None and not url_good:
            queryset.exclude(condition="good")
            print("good")
        if url_acceptable is not None and not url_acceptable:
            queryset.exclude(condition="acceptable")
            print("ok")
        
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

    #these will search in our models for matches
    books = Textbook.objects.filter(title__icontains=search) | Textbook.objects.filter(author__icontains=search) | Textbook.objects.filter(isbn13__icontains=search) | Textbook.objects.filter(isbn10__icontains=search) | Textbook.objects.filter(bookstore_isbn__icontains=search) # TODO: Add other methods to search
    courses = Class.objects.filter(class_info__icontains=search.replace(" ", ""))
    
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
