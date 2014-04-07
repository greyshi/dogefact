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
        # put your own credentials here
        ACCOUNT_SID = "ACc05280a86f26b3e501c2773bda0b8ff5"
        AUTH_TOKEN = "c60430045deb77bddaa548e370cba36a"

        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
        user_log = open(BASE_DIR + '/logs/users.log', 'a')
        error_log = open(BASE_DIR + '/logs/error.log', 'a')


        messages = Message.objects.all()
        for u in User.objects.all():
            if u.current_message >= len(messages):
                user_log.write("{0}, {1}, {2}\n".format(u.phone_number, u.start_date, datetime.datetime.utcnow()))
                u.delete()
            else:
                try:
                    client.messages.create(
                        to=u.phone_number,
                        from_="+15128722226",
                        body=messages[u.current_message].content,
                    )
                except TwilioRestException as e:
                    error_log.write("{0}, {1}, {2}\n".format(u.phone_number, datetime.datetime.utcnow(), e))
                else:
                    u.current_message += 1
                    u.save()
        user_log.close()
        error_log.close()
