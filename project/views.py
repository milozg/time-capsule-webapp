# project/views.py

from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import datetime, random
from django.utils import timezone

def random_datetime(start, end):
    '''A function to return a random datetime between two input datetimes.'''
    start_ts = start.timestamp()
    end_ts = end.timestamp()
    random_ts = random.uniform(start_ts, end_ts)
    return datetime.datetime.fromtimestamp(random_ts)

# Create your views here.

def show_about(request):
    '''Show the about page'''
    context = {}
    if request.user.is_authenticated:
        context['profile'] = Profile.objects.get(user=request.user)

    template_name = 'project/about.html'
    return render(request, template_name, context=context)

class MyLoginRequiredMixin(LoginRequiredMixin):
    '''Change the get_login_url of the default LoginRequiredMixin'''
    def get_login_url(self):
        '''return the login url'''
        return reverse('login')

class ShowProfileHomeView(MyLoginRequiredMixin, DetailView):
    '''A view class to display a detail view of a profile.'''
    model = Profile
    template_name = 'project/profile_home.html'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class CreateProfileView(CreateView):
    '''A view to handle the creation of a new profile'''
    form_class = CreateProfileForm
    template_name = 'project/create_profile_form.html'
    def get_context_data(self):
        context = super().get_context_data()
        userForm = UserCreationForm
        context['userForm'] = userForm
        return context
    def form_valid(self, form):
        print(self.request.POST)
        userForm = UserCreationForm(self.request.POST)
        print(userForm)
        user = userForm.save()
        login(self.request,user)

        form.instance.user = user

        return super().form_valid(form)

class CreatePersonalMessageView(MyLoginRequiredMixin, CreateView):
    '''A view to create a new personal message and save it to the database.'''
    form_class = CreatePersonalMessageForm
    template_name = "project/create_pm_form.html"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new status message'''
        return reverse('profile_home')
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template'''
        context = super().get_context_data()
        profile = self.get_object()
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''Handle the form submission and save the new object to the Django database.'''

        profile = self.get_object()
        form.instance.profile = profile

        dt = random_datetime(form.instance.min_delivery, form.instance.max_delivery)
        dt = dt.astimezone(timezone.get_current_timezone())
        form.instance.delivery_date = dt

        pm = form.save()
        pm.add_at_job()

        return super().form_valid(form)
    
class SearchNewFriendsListView(MyLoginRequiredMixin, ListView):
    '''A class to handle the url to show a template that allows users to search for new friends.'''
    template_name = 'project/new_friends.html'
    model = Profile
    context_object_name = 'profiles'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template'''
        context = super().get_context_data()
        profile = self.get_object()
        context['profile'] = profile
        return context

    def get_queryset(self):
        
        # start with those who profile is not yet friends with
        results = self.get_object().get_not_friends()

        # filter results by these field(s):
        if 'first_name' in self.request.GET:
            first_name = self.request.GET['first_name']
            if first_name:
                results = results.filter(first_name=first_name)
                
        return results
    
class CreateFriendView(MyLoginRequiredMixin, View):
    '''View class to handle the creation of a new friend relationship between two profiles.'''
    model = Profile

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        '''Call the profile1 add friend method.'''

        profile1 = self.get_object()
        profile2 = Profile.objects.get(pk=kwargs['other_pk'])
        profile1.add_friend(profile2)

        return redirect(reverse('profile_home'))