# project/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware, get_current_timezone, is_naive

def at_job_helper(delivery_date, subject, email, message):
    '''A helper function that will add an email at job given the required fields.'''
    # convert delivery date to at time
    at_time = delivery_date.strftime('%H:%M %b %d %Y')

    # New Approach:
    # Add atjobs as sh files to a directory and have a crontab call a script every minute.
    # When the script will go through the directory and add any jobs there as at jobs then
    # remove them.
    job_id = timezone.now().strftime("%Y%m%d%H%M%S.%f")
    command = f'mailx -s \\"{subject}\\" \\"{email}\\" <<< \\"{message}\\"'

    # For local:
    # with open(f'/Users/mish/Desktop/job_queue/{job_id}.sh', 'w') as f:
    #     f.write(f'echo "{command}" | at {at_time}\n')

    # For Server
    with open(f'/home/ugrad/milozg/job_queue/{job_id}.sh', 'w') as f:
        f.write(f'echo "{command}" | at {at_time}\n')

def ensure_aware(dt):
    '''A function to ensure that a datetime is aware and in the correct timezone.'''
    if is_naive(dt):
        return make_aware(dt, timezone=get_current_timezone())
    else:
        return dt.astimezone(timezone.get_current_timezone())

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

        pms = self.get_all_pms().filter(delivery_date__gt=curr_time)
        return pms
    
    def get_delivered_pms(self):
        '''A function to return all personal messages that have been delivered.'''
        curr_time = timezone.now()

        pms = self.get_all_pms().filter(delivery_date__lt=curr_time)
        return pms
    
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
    
    def get_friends(self):
        '''Return a list of all the profiles that this profile is friends with.'''
        friend_relations = Friend.objects.all()
        friend_pks = []

        for rel in friend_relations:
            if rel.profile1 == self:
                friend_pks.append(rel.profile2.pk)
            elif rel.profile2 == self:
                friend_pks.append(rel.profile1.pk)
        
        return Profile.objects.filter(pk__in=friend_pks)
    
    def get_not_friends(self):
        '''Return a queryset of all the profiles that this profile is not friends with.'''

        profiles_to_exclude = list(map(lambda p: p.pk, self.get_friends()))
        profiles_to_exclude.append(self.pk)

        not_friends = Profile.objects.exclude(pk__in=profiles_to_exclude)
        return not_friends
    
    def get_groups(self):
        '''Return a queryset of all the groups that this profile belongs to.'''
        return self.groups.all()
    
    def get_open_groups(self):
        '''Return a queryset of all the groups that the profile is in that are still open to new messages.'''
        curr_time = timezone.now()

        groups = self.get_groups().filter(min_delivery__gt=curr_time)
        return groups
    
    def get_closed_groups(self):
        '''Return a queryset of all the groups that the profile is in that are not accepting new messages.'''
        curr_time = timezone.now()

        groups = self.get_groups().filter(min_delivery__lt=curr_time)
        return groups

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

class Friend(models.Model):
    '''Encapsulate a friendship between two profiles in the Database.'''
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friend1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friend2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile1.first_name} & {self.profile2.first_name}'
    
class Group(models.Model):
    '''Encapsulate a group of profiles that contains group messages.'''
    name = models.TextField(blank=False)
    created = models.DateTimeField(auto_now=True)
    min_delivery = models.DateTimeField(blank=False)
    max_delivery = models.DateTimeField(blank=False)
    delivery_date = models.DateTimeField(blank=True)
    members = models.ManyToManyField(Profile, related_name="groups")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object'''
        return reverse('show_group', kwargs={'pk':self.pk})
    
    def get_messages(self):
        '''Return a queryset of all messages for this group.'''
        gms = GroupMessage.objects.filter(group=self).order_by('-created')
        return gms
    
    def is_closed(self):
        '''
            Return a boolean indicating whether or not the group is closed to new messages
            i.e. the min delivery date has passed and thus new messages cannot be accepted
        '''
        curr_time = timezone.now()
        return self.min_delivery <= curr_time

class GroupMessage(models.Model):
    '''Encapsulate a message for a group that will be sent out with the other messages.'''
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subject = models.TextField(blank=False)
    message = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile}\'s message for {self.group} about {self.subject}'
    
    def add_at_jobs(self):
        '''
            A function to create at jobs that will send this message at a random time in the specified range
            to all members of the group. Will be called once upon the save of this GroupMessage record.
        '''
        subject = f'{self.profile.first_name}\'s message in {self.group.name} about {self.subject}'

        dt = ensure_aware(self.group.delivery_date)

        for member in self.group.members.all():
            at_job_helper(dt, subject, member.email, self.message)