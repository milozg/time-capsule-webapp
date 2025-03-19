# mini_fb/models.py

from django.db import models
from django.urls import reverse

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
    
    def get_all_status_messages(self):
        '''Return a Query set of all the status messages for this profile'''
        msgs = StatusMessage.objects.filter(profile=self).order_by('-published')
        return msgs
    
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object'''
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_friends(self):
        '''Return a list of all the profiles that this profile is friends with.'''
        friend_relations = Friend.objects.all()
        friends = []

        for rel in friend_relations:
            if rel.profile1 == self:
                friends.append(rel.profile2)
            elif rel.profile2 == self:
                friends.append(rel.profile1)
        
        return friends
        
    def add_friend(self, other):
        '''Add a friend relationship for this profile and the one refered to in other, if it is valid.'''
        if other == self:
            return
        if other in self.get_friends():
            return
        
        new_friend = Friend()
        new_friend.profile1 = self
        new_friend.profile2 = other
        new_friend.save()
        return
    
    def get_friend_suggestions(self):
        '''Return a Queryset of friend suggestions for this profile'''

        profiles_to_exclude = list(map(lambda p: p.pk, self.get_friends()))
        profiles_to_exclude.append(self.pk)

        suggestions = Profile.objects.exclude(pk__in=profiles_to_exclude)
        return suggestions
    
    def get_news_feed(self):
        '''Get all status messages for this profile and this profile's friends.'''
        profiles = self.get_friends()
        profiles.append(self)

        feed = StatusMessage.objects.filter(profile__in=profiles).order_by('-published')

        return feed
    
class Friend(models.Model):
    '''Encapsulate a friendship between two profiles in the Database.'''
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile1.first_name} & {self.profile2.first_name}'


class StatusMessage(models.Model):
    '''Encapsulate a status message for a specific profile.'''

    published = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        '''Define a string representaion of this model instance'''
        return f'{self.text}'
    
    def get_images(self):
        '''Return a QuerySet of the images associated with this status message.'''
        return Image.objects.filter(statusimage__status_message=self)
    
    def get_absolute_url(self):
        '''Return a URL to display the profile for this status message.'''


        return reverse('show_profile', kwargs={'pk':self.profile.pk})
        
class Image(models.Model):
    '''Encapsulate an Image posted to the Webapp.'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(blank=False)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''Define a string representaion of this model instance'''
        return f'{self.image}'
    
class StatusImage(models.Model):
    '''Encapsulte a relationship between a image and a status message.'''
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

    def __str__(self):
        '''Define a string representaion of this model instance'''
        return f'{self.image} for {self.status_message}'