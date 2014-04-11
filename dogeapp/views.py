import datetime
import time
import jwt

from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.conf import settings

from models import User, Message, UserForm, DeleteUserForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def success(request):
    return render(request, 'success.html')

def subscribe(request):
    f = UserForm(request.POST)
    try:
        f.clean_phone_number()
    except ValidationError as e:
        return render(request, 'home.html', {'error': e.message})
    u = f.save()
    u.save()

    dogeToken = jwt.encode(
    {
      "iss" : settings.SELLER_ID,
      "aud" : "Google",
      "typ" : "google/payments/inapp/item/v1",
      "exp" : int(time.time() + 3600),
      "iat" : int(time.time()),
      "request" :{
        "name" : "Doge Fact",
        "description" : "A 30-day subscription to Doge Fact for {0}".format(u.phone_number),
        "price" : "1.00",
        "currencyCode" : "USD",
        "sellerData" : "user_id:{0}".format(u.id)
      }
    },
    settings.SELLER_SECRET)
    return render(request, 'subscribe.html', {'user': u, 'token': dogeToken})

@csrf_exempt
def confirm(request):
    if request.method == 'POST':
        payload = request.POST.get('jwt', "")
        if payload:
            postback = jwt.decode(payload, settings.SELLER_SECRET)
            if postback and postback['iss'] == 'Google' and postback['aud'] == settings.SELLER_ID:
                order_id = postback['response']['orderId']
                user_id = int(postback['request']['sellerData'].split(':')[1])
                user = get_object_or_404(User, id=user_id)
                user.confirmation_code = order_id
                user.is_active = True
                user.save()
                return HttpResponse(order_id)
    return HttpResponseRedirect("/")



def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    #+some code to check if this object belongs to the logged in user

    if request.method == 'POST' and request.POST.get('phone_number') == user_to_delete.phone_number:
        form = DeleteUserForm(request.POST, instance=user_to_delete)

        if form.is_valid():
            user_to_delete.delete()
            return HttpResponseRedirect("/") # wherever to go after deleting

    return render(request, 'home.html')
