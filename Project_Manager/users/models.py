from django.db import models
from django.contrib.auth.models import AbstractUser

from project_manager import settings


# Create your models here.

class User(AbstractUser):
    ...

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    tag = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)



class TeamMember(models.Model):
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_joining = models.DateTimeField(auto_now_add=True)


class ProjectMember(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_joining = models.DateTimeField(auto_now_add=True)


class TaskExecutor(models.Model):
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)