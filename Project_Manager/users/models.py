import random
from django.db import models
from django.contrib.auth.models import AbstractUser

from project_manager import settings


def get_colors():
    return ['sky', 'blue', 'red', 'orange', 'lime', 'teal', 'violet', 'zinc']

def get_random_color():
    return random.choice(get_colors())


class User(AbstractUser):
    ...

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)


class Tag(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='tags')
    name = models.CharField(max_length=25, blank=True, null=True)
    color = models.CharField(max_length=25, default=get_random_color)


    @property
    def get_colors(self):
        return f'text-{self.color}-700 bg-{self.color}-200 border-{self.color}-700'


class SocialNetwork(models.Model):
    TELEGRAM = 'Telegram'
    VKONTAKTE = 'VK'
    GITHUB = 'GitHub'

    SOCIAL_CHOICES = [
        (TELEGRAM, 'Telegram'),
        (VKONTAKTE, 'VKontakte'),
        (GITHUB, 'GitHub'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    network = models.CharField(max_length=20, choices=SOCIAL_CHOICES)
    link = models.URLField(max_length=255)

    class Meta:
        unique_together = ('profile', 'network')
    



class TeamMember(models.Model):
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_joining = models.DateTimeField(auto_now_add=True)


class ProjectMember(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='pm')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_joining = models.DateTimeField(auto_now_add=True)


class TaskExecutor(models.Model):
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)