import datetime

from django.shortcuts import render

from models import User, Message


def home(request):
    return render(request, 'home.html')

def create(request):
    messages = Message.objects.all()
    users = User.objects.all()
    return render(request, 'create.html', {'users': users, 'messages': messages})

