# mini_fb/views.py

from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class MyLoginRequiredMixin(LoginRequiredMixin):
    '''Change the get_login_url of the default LoginRequiredMixin'''
    def get_login_url(self):
        '''return the login url'''
        return reverse('login')
    
class ShowMyProfileView(View):
    '''Find the current users profile to redirect to a show profile page view.'''
    model = Profile

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        '''redirect to show the profile of the currently logged in user.'''

        profile1 = self.get_object()

        return redirect(reverse('show_profile', kwargs={'pk' : profile1.pk}))

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
    def get_context_data(self):
        context = super().get_context_data()
        userForm = UserCreationForm
        context['userForm'] = userForm
        return context
    def form_valid(self, form):
        userForm = UserCreationForm(self.request.POST)
        user = userForm.save()
        login(self.request,user)

        form.instance.user = user

        return super().form_valid(form)

class CreateStatusMessageView(MyLoginRequiredMixin, CreateView):
    '''A view to create a new status message and save it to the database.'''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new status message'''
        pk = self.get_object().pk
        return reverse('show_profile', kwargs={'pk' : pk})
    
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

        # print(f'CreateSMView: form.cleaned_data={form.cleaned_data}')

        sm = form.save()
        files = self.request.FILES.getlist('files')
        # print(files)
        for f in files:
            new_img = Image()
            new_img.image = f
            new_img.profile = profile
            new_img.save()

            new_si = StatusImage()
            new_si.image = new_img
            new_si.status_message = sm
            new_si.save()

        return super().form_valid(form)
    
class UpdateProfileView(MyLoginRequiredMixin, UpdateView):
    '''View class to handle the update of a profile in the DB.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class DeleteStatusMessageView(MyLoginRequiredMixin, DeleteView):
    '''View class to delete a status message on a profile'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status'

    def get_success_url(self):
        '''Return the URL to direct to after a successful delete.'''

        pk = self.kwargs['pk']
        sm = StatusMessage.objects.get(pk=pk)
        profile = sm.profile

        return reverse('show_profile', kwargs={'pk' : profile.pk})
    
class UpdateStatusMessageView(MyLoginRequiredMixin, UpdateView):
    '''View class to handle the update of a status message in the DB.'''
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    context_object_name = 'status'

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

        return redirect(reverse('show_profile', kwargs={'pk' : profile1.pk}))

class ShowFriendSuggestionsView(MyLoginRequiredMixin, DetailView):
    '''View class to handle the request to display the friend suggestions for a profile'''

    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class ShowNewsFeedView(MyLoginRequiredMixin, DetailView):
    '''View class to handle the request to see the news feed of a profile'''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)