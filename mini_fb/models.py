# mini_fb/models.py

from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a profile.'''

    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Define a string representaion of this model instance'''
        return f'{self.first_name} {self.last_name}'
