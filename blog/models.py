# blog/models.py

from django.db import models

# Create your models here.
class Article(models.Model):
    '''Encapsulate the data of an article written by an author'''

    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Define a string representaion of this model instance'''
        return f'{self.title} by {self.author}'