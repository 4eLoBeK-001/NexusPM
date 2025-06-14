import random

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from projects.models import Project

def get_colors():
    return ['sky', 'blue', 'red', 'orange', 'lime', 'teal', 'violet', 'zinc']

def get_random_color():
    return random.choice(get_colors())


class Task(models.Model):
    class PriprityChoices(models.TextChoices):
        HIGHEST = 'Самый высокий'
        HIGH = 'Высокий'
        MEDIUM = 'Средний'
        LOW = 'Низкий'
        LOWEST = 'Самый низкий'
        NOT_SPECIFIED = 'Не указан'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=10, default=get_random_color)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='creator', null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='tasks', null=True)
    tag = models.ManyToManyField('Tag', related_name='tags', null=True, blank=True)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, related_name='statuses', default='Новая', null=True)
    priority = models.CharField(max_length=20, choices=PriprityChoices.choices, default=PriprityChoices.NOT_SPECIFIED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=25)
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tags', null=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=25, blank=False)
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True, blank=False)
    is_completed = models.BooleanField(default=False, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='statuses', null=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)
    color_name = models.CharField(max_length=50)
    bg_color = models.CharField(max_length=50)
    text_color = models.CharField(max_length=50)
    border_color = models.CharField(max_length=50)

    def __str__(self):
        return self.name
