from django.shortcuts import render

def complete(request):
    context=get_logged_in(request)

    return render(request, 'textbook_exchange/landing.html', context=context)

def redirect(request):
    context=get_logged_in(request)

    return render(request, 'textbook_exchange/landing.html', context=context)
