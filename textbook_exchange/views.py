from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request, 'textbook_exchange/landing.html')

def buy_books(request):
    return render(request, 'textbook_exchange/buybooks.html', {'title': 'Buy Books'})