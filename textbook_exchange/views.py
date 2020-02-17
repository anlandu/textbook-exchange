from django.shortcuts import render

# Create your views here.
def landing(request):
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
    return render(request, 'textbook_exchange/landing.html', context=context)

def buy_books(request):
    logged_in = request.session.get("email_domain", "")
    if logged_in == "virginia.edu":
        context = {
            'title': 'Buy Books',
            'logged_in': True,
            'account': request.session.get('current_email', ''),
        }
    else:
        context = {
            'title': 'Buy Books',
            'logged_in': False,
        }
    return render(request, 'textbook_exchange/buybooks.html', context=context)