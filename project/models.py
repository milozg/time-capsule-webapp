# project/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

def at_job_helper(delivery_date, subject, email, message):
    '''A helper function that will add an email at job given the required fields.'''
    # convert delivery date to at time
    at_time = delivery_date.strftime('%H:%M %b %d %Y')

    # New Approach:
    # Add atjobs as sh files to a directory and have a crontab call a script every minute.
    # When the script will go through the directory and add any jobs there as at jobs then
    # remove them.
    job_id = timezone.now().strftime("%Y%m%d%H%M%S")
    command = f'mailx -s \\"{subject}\\" \\"{email}\\" <<< \\"{message}\\"'

    # For local:
    # with open(f'/Users/mish/Desktop/job_queue/{job_id}.sh', 'w') as f:
    #     f.write(f'echo "{command}" | at {at_time}\n')

    # For Server
    with open(f'/home/ugrad/milozg/job_queue/{job_id}.sh', 'w') as f:
        f.write(f'echo "{command}" | at {at_time}\n')

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data for a profile.'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=True)
    email = models.TextField(blank=False)
    profile_pic = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='capsule_profile')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object'''
        return reverse('profile_home')
    
    def get_all_pms(self):
        '''A function to return all personal messages associated with this profile.'''
        pms = PersonalMessage.objects.filter(profile=self).order_by('-created')
        return pms
    
    def get_undelivered_pms(self):
        '''A function to return all personal messages that have not yet been delivered.'''
        curr_time = timezone.now()

        pms = PersonalMessage.objects.filter(profile=self, delivery_date__gt=curr_time)
        return pms
    
    def get_delivered_pms(self):
        '''A function to return all personal messages that have been delivered.'''
        curr_time = timezone.now()

        pms = PersonalMessage.objects.filter(profile=self, delivery_date__lt=curr_time)
        return pms

class PersonalMessage(models.Model):
    '''Encapsulate the data of a message a profile makes to themselves.'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subject = models.TextField(blank=False)
    message = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)
    min_delivery = models.DateTimeField(blank=False)
    max_delivery = models.DateTimeField(blank=False)
    delivery_date = models.DateTimeField(blank=True)

    def __str__(self):
        return f'{self.subject}'
    
    def add_at_job(self):
        '''A function to create an at job that will send this message at a random time in the specified range.
            Will be called once upon the save of this PersonalMessage record.
        '''
        at_job_helper(self.delivery_date, self.subject, self.profile.email, self.message)
