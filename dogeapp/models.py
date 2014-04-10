import string

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError


class User(models.Model):
    phone_number = models.CharField(max_length=500)
    start_date = models.DateTimeField('subscription start date', auto_now=True)
    current_message = models.PositiveSmallIntegerField(default=0)
    confirmation_code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)


    def __unicode__(self):
        return self.phone_number

    class Meta:
        ordering = ['start_date']
        verbose_name_plural = "Users"


class Message(models.Model):
    content = models.TextField()
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
            raise ValidationError("You didn't type a phone number!")
        phone_number = ""
        for c in input_number:
            if c in string.digits:
                phone_number += c
            elif c not in string.punctuation:
                raise ValidationError("The number you entered was invalid. Please try again.")

        if len(phone_number) < 10:
            raise ValidationError("The phone number you entered was too short. Please try again.")
        if len(phone_number) > 15:
            raise ValidationError("The phone number you entered was too long. Please try again.")
        return input_number


class DeleteUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['phone_number']
