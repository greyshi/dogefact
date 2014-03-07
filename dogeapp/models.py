import string

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError


class User(models.Model):
    phone_number = models.CharField(max_length=500)
    start_date = models.DateTimeField('subscription start date', auto_now=True)
    current_message = models.PositiveSmallIntegerField(default=0)

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
        ordering = ['pub_date']
        verbose_name_plural = "Messages"


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['phone_number']

    def clean_phone_number(self):
        input_number = self['phone_number'].value()
        if not input_number:
            raise ValidationError("You forgot to type the phone number!")
        phone_number = [d for d in input_number if d in string.digits]
        if len(phone_number) < 10:
            raise ValidationError("The phone number you entered was too short! Please try again.")
        if len(phone_number) > 15:
            raise ValidationError("The phone number you entered was too long! Please try again.")
        return input_number

