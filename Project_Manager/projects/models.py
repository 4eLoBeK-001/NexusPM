from django.db import models
from django.contrib.auth import get_user_model

from teams.models import Team

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='project_avatars/', blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='projects', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)