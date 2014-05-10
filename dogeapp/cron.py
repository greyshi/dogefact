import datetime

from django_cron import CronJobBase, Schedule
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
from models import User, Message
from dogehouse.settings import BASE_DIR

import smtplib  
from email.mime.text import MIMEText
  

class SendMessages(CronJobBase):
    RUN_EVERY_MINS = 1
    RUN_AT_TIMES = ['0:31']

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, run_at_times=RUN_AT_TIMES)
    code = 'dogeapp.send_messages'    # a unique code

    def do(self):
        ACCOUNT_SID = "ACc05280a86f26b3e501c2773bda0b8ff5"
        AUTH_TOKEN = "c60430045deb77bddaa548e370cba36a"

        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

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

        messages = Message.objects.all()
        for u in User.objects.filter(is_active=True):
            if u.current_message >= len(messages):
                u.is_active = False
                u.save()
            else:
                try:
                    client.messages.create(
                        to=u.phone_number,
                        from_="+15128722226",
                        body=messages[u.current_message].content,
                    )
                except (TwilioRestException, Exception) as e:
                    if "21610" not in e.message:
                        msg = MIMEText("{0}\n{1}\n\n{2}".format(u.phone_number, datetime.datetime.utcnow(), e))
                        msg['Subject'] = "Dogefact Failure"
                        msg['From'] = from_address
                        msg['To'] = to_address
                        # Send Mail
                        server.sendmail(from_address, [to_address, to_address_2], msg.as_string())  
                else:
                    u.current_message += 1
                    u.save()
        server.quit()
