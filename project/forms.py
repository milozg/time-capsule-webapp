# project/forms.py

from django import forms
from .models import *
from formset.widgets import DateTimeInput

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'profile_pic']

class CreatePersonalMessageForm(forms.ModelForm):
    '''A form to add a PersonalMessage to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = PersonalMessage
        fields = ['subject', 'message', 'min_delivery', 'max_delivery']
        widgets = {
            'min_delivery':DateTimeInput,
            'max_delivery':DateTimeInput,
        }
