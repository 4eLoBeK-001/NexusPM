import random

from django.db import models
from django.contrib.auth import get_user_model

from projects.models import Project

def get_colors():
    return ['sky', 'blue', 'red', 'orange', 'lime', 'teal', 'violet', 'zinc']

def get_random_color():
    return random.choice(get_colors())


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=10, default=get_random_color)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='creator', null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='tasks', null=True)
    tag = models.ManyToManyField('Tag', related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=25)
    color = models.ForeignKey('TagColor', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class TagColor(models.Model):
    name = models.CharField(max_length=50)
    bg_color = models.CharField(max_length=50)
    text_color = models.CharField(max_length=50)
    border_color = models.CharField(max_length=50)

    def __str__(self):
        return self.name
