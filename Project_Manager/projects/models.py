import random

from django.db import models
from django.contrib.auth import get_user_model

from teams.models import Team


def get_colors():
    return ['sky', 'blue', 'red', 'orange', 'lime', 'teal', 'violet', 'zinc']

def get_random_color():
    return random.choice(get_colors())

class Project(models.Model):
    class StatusChoices(models.TextChoices):
        IN_WORK = 'В работе'
        STOPPED = 'Приостановлен'
        COMPLETED = 'Завершён'

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='project_avatars/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.IN_WORK)
    color = models.CharField(max_length=10, default=get_random_color)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='projects', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def short_name(self):
        return self.name[:2].upper()