from django.db import models
from django.contrib.auth import get_user_model



class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('team_deleted', 'Команда удалена'),
        ('team_changed_name', 'Изменение названия команды'),
        ('team_changed_description', 'Изменение описание команды'),
        ('team_changed_photo', 'Изменение фото команды'),
        ('team_member_joined', 'Присоединение к команде'),
        ('team_member_role_changed', 'Изменение роли'),
        ('team_member_left', 'Покинул команду'),
        ('project_created', 'Создание проекта'),
        ('project_changed_name', 'Изменение названия проекта'),
        ('project_changed_description', 'Изменение описание проекта'),
        ('project_changed_photo', 'Изменение фото проекта'),
        ('project_changed_status', 'Изменение статуса проекта'),
        ('project_deleted', 'Удаление проекта'),
        ('subtask_created', 'Создана задача'),
        ('task_created', 'Создана задача'),
        ('task_deleted', 'Задача удалена'),
        ('team_changed_name', 'Изменение названия задачи'),
        ('team_changed_description', 'Изменение описания задачи'),
        ('team_changed_status', 'Изменение статуса задачи'),
        ('team_changed_priority', 'Изменение приоритета задачи'),
        ('task_executor_changed', 'Изменены исполнители'),
        ('task_no_executor', 'Исполнителей нет'),
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

        if self.action_type == 'team_deleted':
            string = f'Команда {self.team.name if self.project else self.data.get('team_name')} была удалена'
            return string
        if self.action_type == 'team_changed_name':
            string = f'Пользователь {self.user.username} изменил название команды {self.data.get('old')} на {self.data.get('new')}'
            return string
        if self.action_type == 'team_changed_description':
            string = f'Пользователь {self.user.username} изменил описание команды {self.team.name if self.project else self.data.get('team_name')} с {self.data.get('old')} на {self.data.get('new')}'
            return string

        if self.action_type == 'team_changed_photo':
            string = f'Пользователь {self.user.username} изменил фото команды {self.team.name if self.project else self.data.get('team_name')}'
            return string

        if self.action_type == 'team_member_joined':
            string = f'Пользователь {self.user.username} вступил в команду {self.team.name if self.project else self.data.get('team_name')}'
            return string

        if self.action_type == 'team_member_role_changed':
            string = f'У {self.user.username} была сменена роль с {self.data.get('old')} на {self.data.get('new')}'
            return string

        if self.action_type == 'team_member_left':
            string = f'Пользователь {self.user.username} покинул команду {self.team.name if self.project else self.data.get('team_name')}'
            return string

        if self.action_type == 'project_created':
            string = f'{self.user.username} создал проект {self.project.name if self.project else self.data.get('project_name')}'
            return string

        if self.action_type == 'project_changed_name':
            string = f'{self.user.username} изменил имя проекта "{self.data.get('old')}" на "{self.data.get('new')}"'
            return string

        if self.action_type == 'project_changed_description':
            string = f'{self.user.username} изменил описание проекта "{self.data.get('old')}" на "{self.data.get('new')}"'
            return string

        if self.action_type == 'project_changed_photo':
            string = f'{self.user.username} изменил фото проекта {self.project.name if self.project else self.data.get('project_name')}'
            return string
        
        if self.action_type == 'project_changed_status':
            string = f'{self.user.username} изменил статус проекта {self.project.name if self.project else self.data.get('project_name')} с "{self.data.get('old')}" на "{self.data.get('new')}"'
            return string
        
        if self.action_type == 'project_deleted':
            string = f'{self.user.username} удалил проект {self.project.name if self.project else self.data.get('project_name')}'
            return string

        if self.action_type == 'task_created':
            string = f'{self.user.username} создал задачу {self.task.name}'
            return string
        
        if self.action_type == 'subtask_created':
            string = f'{self.user.username} создал подзадачу {self.task.name} к задаче {self.task.parent_task.name}'
            return string
        
        if self.action_type == 'task_deleted':
            string = f'{self.user.username} удалил задачу {self.task.name}'
            return string

        if self.action_type == 'team_changed_name':
            string = f'{self.user.username} изменил имя задачи с {self.data.get('old')} на {self.data.get('new')}'
            return string
        
        if self.action_type == 'team_changed_description':
            string = f'{self.user.username} изменил описание задачи {self.task.name} с {self.data.get('old')} на {self.data.get('new')}'
            return string
        
        if self.action_type == 'team_changed_status':
            string = f'{self.user.username} изменил статус задачи {self.task.name} с {self.data.get('old')} на {self.data.get('new')}'
            return string
        
        if self.action_type == 'team_changed_priority':
            string = f'{self.user.username} изменил приоритет задачи {self.task.name} с {self.data.get('old')} на {self.data.get('new')}'
            return string

        if self.action_type == 'task_executor_changed':
            string = f'За задачу {self.task.name} назначены исполнители {self.data.get('data')}'
            return string

        if self.action_type == 'task_no_executor':
            string = f'У задачи {self.task.name} больше нет исполнителей'
            return string

        if self.action_type == 'tag_created':
            string = f'{self.user.username} создал новый тег {self.data.get('data')}'
            return string

        if self.action_type == 'tag_deleted':
            string = f'{self.user.username} удалил тег {self.data.get('data')}'
            return string

        if self.action_type == 'task_tag_changed':
            string = f'{self.user.username} в задаче {self.task.name} изменил теги: {self.data.get('data')}'
            return string

        if self.action_type == 'status_created':
            string = f'{self.user.username} создал новый статус {self.data.get('data')}'
            return string

        if self.action_type == 'status_deleted':
            string = f'{self.user.username} удалил статус {self.data.get('data')}'
            return string

        if self.action_type == 'comment_created':
            string = f'{self.user.username} оставил комментарие к задаче {self.task.name}: {self.data.get('data')}'
            return string

        if self.action_type == 'comment_deleted':
            string = f'{self.user.username} удалил комментарий к задаче {self.task.username}'
            return string

    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'История действия'
        verbose_name_plural = 'История действий'