import datetime
from django.db import models


class User(models.Model):
    phone_number = models.CharField(max_length=500)
    start_date = models.DateTimeField('subscription start date', auto_now=True)
    expiration_date = models.DateTimeField('date the subscription expires')

    def __unicode__(self):
        return self.phone_number

    class Meta:
        ordering = ['start_date']
        verbose_name_plural = "Users"


class Message(models.Model):
    content = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published', auto_now_add=True,)

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = "Messages"

