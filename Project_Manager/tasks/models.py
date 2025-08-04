import random

from django.db import models
from django.contrib.auth import get_user_model

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
    tag = models.ManyToManyField('Tag', related_name='tags', blank=True)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, related_name='statuses', default='Новая', null=True)
    priority = models.CharField(max_length=20, choices=PriprityChoices.choices, default=PriprityChoices.NOT_SPECIFIED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')
    executor = models.ManyToManyField(get_user_model(), through='users.TaskExecutor', related_name='assigned_tasks', blank=True)


    class Meta:
        ordering = ('-created_at', 'name')
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.parent_task and self.parent_task.parent_task:
            raise ValidationError('Допустима только одна вложенность подзадач')
    
    def __str__(self):
        return self.name
    
    @property
    def get_priority_color(self):
        return {
            self.PriprityChoices.HIGHEST: 'bg-red-600 text-red-950 border-rose-700',
            self.PriprityChoices.HIGH: 'bg-red-500 text-red-900 border-red-800',
            self.PriprityChoices.MEDIUM: 'bg-amber-500 text-orange-700 border-orange-700',
            self.PriprityChoices.LOW: 'bg-green-500 text-green-900 border-green-800',
            self.PriprityChoices.LOWEST: 'bg-emerald-400 text-emerald-800 border-emerald-700',
            self.PriprityChoices.NOT_SPECIFIED: 'bg-indigo-300 text-slate-800 border-indigo-900',
        }.get(self.priority)


class TaskImage(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='task_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Вложение к задаче {self.task}'
    
    class Meta:
        ordering = ('-uploaded_at',)
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'


class Tag(models.Model):
    name = models.CharField(max_length=25)
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tags', null=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=25, blank=False)
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True, blank=False)
    is_completed = models.BooleanField(default=False, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='statuses', null=True)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)
    color_name = models.CharField(max_length=50)
    bg_color = models.CharField(max_length=50)
    text_color = models.CharField(max_length=50)
    border_color = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='comcreator', null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', 'task')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author} на {self.task}'
