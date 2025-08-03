from django.db import models
from django.contrib.auth import get_user_model



class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('team_changed', 'Изменения в команде'),
        ('team_member_joined', 'Присоединение к команде'),
        ('team_member_left', 'Покинул команду'),
        ('project_created', 'Создание проекта'),
        ('project_changed', 'Изменения проекта'),
        ('project_deleted', 'Удаление проекта'),
        ('task_created', 'Создана задача'),
        ('task_deleted', 'Задача удалена'),
        ('tack_changed', 'Изменение задачи'),
        ('task_executor_changed', 'Изменены исполнители'),
        ('tag_created', 'Создан тег'),
        ('tag_deleted', 'Удалён тег'),
        ('task_tag_changed', 'У задачи поменялись теги'),
        ('status_created', 'Создан статус'),
        ('status_deleted', 'Статус удалён'),
        ('comment_created', 'Создан комментарий'),
        ('comment_deleted', 'Комментарий удалён'),
    ]
    
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey('teams.Team', on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey('tasks.Task', on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=100, choices=ACTION_CHOICES)
    data = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Логирование {self.user}'
    
    class Meta:
        verbose_name = 'История действия'
        verbose_name_plural = 'История действий'