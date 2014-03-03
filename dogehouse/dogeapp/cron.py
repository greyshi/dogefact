from django_cron import CronJobBase, Schedule
import random


class SendMessages(CronJobBase):
    RUN_EVERY_MINS = 1
    RUN_AT_TIMES = ['0:31']

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, run_at_times=RUN_AT_TIMES)
    code = 'dogeapp.send_messages'    # a unique code

    def do(self):
        f = open('/Users/arash/projects/dogefact/dogehouse/foooo' + str(random.randint(500, 5000000)), 'w')
        f.write("hello")
        f.close()