import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from models import User, Message, UserForm


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def subscribe(request):
    f = UserForm(request.POST)
    try:
        f.clean_phone_number()
    except ValidationError as e:
        return render(request, 'home.html', {'error': e.message})
    f.save()
    return render(request, 'subscribe.html', {'phone_number': f['phone_number'].value()})

