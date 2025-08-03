from django.db import models
from django.contrib.auth import get_user_model



class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('team_changed_name', 'Изменение названия команды'),
        ('team_changed_description', 'Изменение описание команды'),
        ('team_changed_photo', 'Изменение фото команды'),
        ('team_member_joined', 'Присоединение к команде'),
        ('team_member_role_changed', 'Изменение роли'),
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
    
    
    def get_html(self):

        if self.action_type == 'team_changed_name':
            string = f'Пользователь {self.user.username} изменил название команды {self.data.get('old')} на {self.data.get('new')}'
            return string
        if self.action_type == 'team_changed_description':
            string = f'Пользователь {self.user.username} изменил описание команды {self.team.name} с {self.data.get('old')} на {self.data.get('new')}'
            return string

        if self.action_type == 'team_changed_photo':
            string = f'Пользователь {self.user.username} изменил фото команды {self.team.name}'
            return string

        if self.action_type == 'team_member_joined':
            string = f'Пользователь {self.user.username} вступил в команду {self.team.name}'
            return string

        if self.action_type == 'team_member_role_changed':
            string = f'Команда {self.team.name}. У {self.user.username} была сменена роль с {self.data.get('old')} на {self.data.get('new')}'
            return string

        if self.action_type == 'team_member_left':
            string = f'Пользователь {self.user.username} покинул команду {self.team.name}'
            return string

        if self.action_type == 'project_created':
            ...

        if self.action_type == 'project_changed':
            ...

        if self.action_type == 'project_deleted':
            ...

        if self.action_type == 'task_created':
            ...

        if self.action_type == 'task_deleted':
            ...

        if self.action_type == 'tack_changed':
            ...

        if self.action_type == 'task_executor_changed':
            ...

        if self.action_type == 'tag_created':
            ...

        if self.action_type == 'tag_deleted':
            ...

        if self.action_type == 'task_tag_changed':
            ...

        if self.action_type == 'status_created':
            ...

        if self.action_type == 'status_deleted':
            ...

        if self.action_type == 'comment_created':
            ...

        if self.action_type == 'comment_deleted':
            ...

    
    class Meta:
        verbose_name = 'История действия'
        verbose_name_plural = 'История действий'