import datetime

from django.shortcuts import render, redirect

from models import User, Message, UserForm


def home(request):
    return render(request, 'home.html')


def subscribe(request):
    f = UserForm(request.POST)
    f.save()
    return redirect('home')

