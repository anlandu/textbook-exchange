from django.shortcuts import render
from django.views import generic

def get_logged_in(request):
    logged_in = request.session.get("email_domain", "")
    if logged_in == "virginia.edu":
        context = {
            'logged_in': True,
            'account': request.session.get('current_email', ''),
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
    context['title']='Buy Books'

    return render(request, 'textbook_exchange/buybooks.html', context=context)

def sell_books(request):
    context=get_logged_in(request)
    context['title']='Sell Books'
    
    return render(request, 'textbook_exchange/sell.html', context=context)
