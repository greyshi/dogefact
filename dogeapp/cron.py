import datetime

from django_cron import CronJobBase, Schedule
from twilio.rest import TwilioRestClient
from models import User, Message


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

        messages = Message.objects.all()
        for u in User.objects.all():
            if u.current_message > 30:
                # log phone number and date to users.log
                # delete the user
                pass
            client.messages.create(
                to=u.phone_number,
                from_="+15128722226",
                body=messages[u.current_message].content,
            )
            u.current_message += 1
            u.save()
