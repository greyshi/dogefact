import datetime
import time
import smtplib  

import jwt

from email.mime.text import MIMEText

from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
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
        "name" : "EvoFacts",
        "description" : "A 15-day subscription to EvoFacts for {0}".format(u.phone_number),
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

                ACCOUNT_SID = "ACc05280a86f26b3e501c2773bda0b8ff5"
                AUTH_TOKEN = "c60430045deb77bddaa548e370cba36a"
                client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

                try:
                    client.messages.create(
                        to=user.phone_number,
                        from_="+15128722226",
                        body=Message.objects.first().content,
                    )
                except (TwilioRestException, Exception) as e:
                    from_address = 'dogefact@gmail.com'  
                    to_address  = 'arashghoreyshi@gmail.com'
                    to_address_2  = 'zakkeener@gmail.com'
                      
                    # Gmail Credentials
                    username = 'dogefact@gmail.com'
                    password = 'dogepassword'
                    server = smtplib.SMTP('smtp.gmail.com:587')  
                    server.ehlo()
                    server.starttls()  
                    server.ehlo()
                    server.login(username,password)  
                    msg = MIMEText("{0}\n{1}\n\n{2}".format(user.phone_number, datetime.datetime.utcnow(), e))
                    msg['Subject'] = "Dogefact Failure"
                    msg['From'] = from_address
                    msg['To'] = to_address
                    # Send Mail
                    server.sendmail(from_address, [to_address, to_address_2], msg.as_string())  
                else:
                    user.current_message += 1

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
