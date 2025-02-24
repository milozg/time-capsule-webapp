# mini_fb/views.py

from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView
from .models import *
from .forms import *

# Create your views here.
class ShowAllProfilesView(ListView):
    '''Define a view class to show all Profiles'''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''Display a single profile.'''

    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    '''A view to handle the creation of a new profile'''
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'