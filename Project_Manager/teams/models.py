import random

from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

def get_random_color():
    return random.choice(['sky', 'blue', 'red', 'orange', 'lime', 'teal', 'violet', 'zinc'])

class Team(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='team_avatars/', blank=True, null=True)
    color = models.CharField(max_length=10, default=get_random_color)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    @property
    def short_name(self):
        return self.name[:2].upper()

    def __str__(self):
        return f'Пороект - {self.name}'
