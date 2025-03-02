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

class CreateStatusMessageView(CreateView):
    '''A view to create a new status message and save it to the database.'''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new status message'''
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk' : pk})
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template'''
        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    
    def form_valid(self, form):
        '''Handle the form submission and save the new object to the Django database.'''

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        # print(f'CreateSMView: form.cleaned_data={form.cleaned_data}')

        sm = form.save()
        files = self.request.FILES.getlist('files')
        print(files)
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