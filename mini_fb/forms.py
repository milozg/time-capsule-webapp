# mini_fb/forms.py

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database'''

    class Meta:
        '''Associate this form with a model from our database'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a status message about a profile'''

    class Meta:
        '''Associate this form with the StatusMessage model'''
        model = StatusMessage
        fields = ['text']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a profile in the database'''

    class Meta:
        '''Associate this form with a model from our database'''
        model = Profile
        fields = ['city', 'email', 'image_url']

class UpdateStatusMessageForm(forms.ModelForm):
    '''A form to update a status message in the database.'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = StatusMessage
        fields = ['text']