import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

from models import User, Message, UserForm, DeleteUserForm


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
    u = f.save()
    return render(request, 'subscribe.html', {'user': u})

def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    #+some code to check if this object belongs to the logged in user

    if request.method == 'POST' and request.POST.get('phone_number') == user_to_delete.phone_number:
        form = DeleteUserForm(request.POST, instance=user_to_delete)

        if form.is_valid():
            user_to_delete.delete()
            return HttpResponseRedirect("/") # wherever to go after deleting

    return render(request, 'home.html')
