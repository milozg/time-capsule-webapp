# project/forms.py

from django import forms
from .models import *
# from formset.widgets import DateTimeInput

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
        # Add widgets to give datetime inputs a calendar input
        widgets = {
            'min_delivery':forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'max_delivery':forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CreateGroupForm(forms.ModelForm):
    '''A form to add a Group to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = Group
        fields = ['name', 'members', 'min_delivery', 'max_delivery']
        # Add datetime widgets and also a checkbox for the members select
        widgets = {
            'min_delivery':forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'max_delivery':forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'members':forms.CheckboxSelectMultiple,

        }
    
    def __init__(self, *args, **kwargs):
        '''Initalize the form, and filter the options for the members to be only the friends of the current profile.'''
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        curr_profile = Profile.objects.get(user=request.user)

        self.fields['members'].queryset = curr_profile.get_friends()

class CreateGroupMessageForm(forms.ModelForm):
    '''A form to add a GroupMessage to the database'''
    class Meta:
        '''Associate this form with a model from our database'''
        model = GroupMessage
        fields = ['subject', 'message']