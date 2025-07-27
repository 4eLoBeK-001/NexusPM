import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

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
    profile_picture = models.ImageField(upload_to='users/profile_pictures/', null=True, blank=True)

    # self.profile_picture = 'users/profile_pictures/avatar.html'
    # lst = ('C:\\', 'Users', 'user', 'Desktop', 'test', 'Project_Manager', 'Project_Manager', 'media')

    @property
    def get_profile_picture_url(self):
        if not self.profile_picture:
            return static('users/default_avatar/avatar.png')
        return self.profile_picture.url
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user}'


class Tag(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='tags')
    name = models.CharField(max_length=25, blank=True, null=True)
    color = models.CharField(max_length=25, default=get_random_color)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


    @property
    def get_colors(self):
        return f'text-{self.color}-700 bg-{self.color}-200 border-{self.color}-700'
    
    def __str__(self):
        return f'Тег {self.name}'


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
        ordering = ('network',)
        unique_together = ('profile', 'network')
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'
    
    @property
    def get_fa_name(self):
        return {
            'Telegram': 'fa-telegram text-blue-500',
            'VK': 'fa-vk text-blue-700',
            'GitHub': 'fa-github text-black',
        }.get(self.network)

    def __str__(self):
        return f'{self.network} на {self.profile.user}'
    



class TeamMember(models.Model):
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_joining = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_joining',)
        verbose_name = 'Участник команды'
        verbose_name_plural = 'Участники команд'

    def __str__(self):
        return f'{self.user} в команде {self.team}'


class ProjectMember(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='pm')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_joining = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_joining',)
        verbose_name = 'Участник проекта'
        verbose_name_plural = 'Участники проектов'

    def __str__(self):
        return f'{self.user} в проекте {self.project}'


class TaskExecutor(models.Model):
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='exec')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='execs')
    
    def __str__(self):
        return f'{self.user} ответственен за {self.task}'