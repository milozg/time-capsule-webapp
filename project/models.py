# project/models.py

from django.db import models
from django.contrib.auth.models import User
import subprocess
from django.urls import reverse
from django.utils import timezone



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

        # convert delivery date to at time
        at_time = self.delivery_date.strftime('%H:%M %b %d %Y')


        # Original code below, did not have permissions on server to create at jobs from
        # django. Will try a different approach

        # Code for when on server:
        # 
        # command = f'mailx -s \\"{self.subject}\\" \\"{self.profile.email}\\" <<< \\"{self.message}\\"'
        # process = subprocess.Popen(
        #     ['at', at_time],
        #     user=421387,
        #     stdin=subprocess.PIPE,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE
        # )
        # stdout, stderr = process.communicate(input=command.encode())

        # Code for when local:
        # 
        # command = f'echo "mailx -s \\"{self.subject}\\" \\"{self.profile.email}\\" <<< \\"{self.message}\\"" > /Users/mish/Desktop/test.txt'
        # process = subprocess.Popen(
        #     ['at', at_time],
        #     stdin=subprocess.PIPE,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE
        # )
        # stdout, stderr = process.communicate(input=command.encode())

        # New Approach:
        # Add atjobs as sh files to a directory and have a crontab call a script every minute.
        # When the script will go through the directory and add any jobs there as at jobs then
        # remove them.

        # For local:
        # job_id = timezone.now().strftime("%Y%m%d%H%M%S")
        # command = f'echo "mailx -s \\"{self.subject}\\" \\"{self.profile.email}\\" <<< \\"{self.message}\\"" > /Users/mish/Desktop/test.txt'

        # with open(f'/Users/mish/Desktop/job_queue/{job_id}.sh', 'w') as f:
        #     f.write(f'echo "{command}" | at {at_time}\n')

        # For Server
        job_id = timezone.now().strftime("%Y%m%d%H%M%S")
        command = f'mailx -s "{self.subject}" "{self.profile.email}" <<< "{self.message}"'

        with open(f'/home/ugrad/milozg/job_queue/{job_id}.sh', 'w') as f:
            f.write(f'echo "{command}" | at {at_time}\n')
