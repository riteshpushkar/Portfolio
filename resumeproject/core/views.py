from django.shortcuts import render

from django.http import HttpResponse
from django.core.mail import send_mail
# from django.conf import settings import Contact
# from .models

# Create your views here.
def home(request) :
    context = {'home': 'active'}
    return render(request, 'core/home.html', context)

def contact(request) :
    context = {'contact': 'active'}

    return render(request, 'core/contact.html', context)