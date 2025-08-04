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
        ('task_created', 'Создана задача'),
        ('subtask_created', 'Создана подзадача'),
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

        username = self.user.username

        name_or_data = lambda obj, key: getattr(self, obj).name if getattr(self, obj) else self.data.get(f'{key}_name')

        actions = {
            'team_deleted': lambda: f'Команда {name_or_data("team", "team")} была удалена',
            'team_changed_name': lambda: f'Пользователь {username} изменил название команды {self.data.get("old")} на {self.data.get("new")}',
            'team_changed_description': lambda: f'Пользователь {username} изменил описание команды {name_or_data("team", "team")} с {self.data.get("old")} на {self.data.get("new")}',
            'team_changed_photo': lambda: f'Пользователь {username} изменил фото команды {name_or_data("team", "team")}',
            'team_member_joined': lambda: f'Пользователь {username} вступил в команду {name_or_data("team", "team")}',
            'team_member_role_changed': lambda: f'У {username} была сменена роль с {self.data.get("old")} на {self.data.get("new")}',
            'team_member_left': lambda: f'Пользователь {username} покинул команду {name_or_data("team", "team")}',
            'project_created': lambda: f'{username} создал проект {name_or_data("project", "project")}',
            'project_changed_name': lambda: f'{username} изменил имя проекта "{self.data.get("old")}" на "{self.data.get("new")}"',
            'project_changed_description': lambda: f'{username} изменил описание проекта "{self.data.get("old")}" на "{self.data.get("new")}"',
            'project_changed_photo': lambda: f'{username} изменил фото проекта {name_or_data("project", "project")}',
            'project_changed_status': lambda: f'{username} изменил статус проекта {name_or_data("project", "project")} с "{self.data.get("old")}" на "{self.data.get("new")}"',
            'project_deleted': lambda: f'{username} удалил проект {name_or_data("project", "project")}',
            'task_created': lambda: f'{username} создал задачу {name_or_data("task", "task")}',
            'subtask_created': lambda: f'{username} создал подзадачу {name_or_data("task", "task")}',
            'task_deleted': lambda: f'{username} удалил задачу {name_or_data("task", "task")}',
            'team_changed_status': lambda: f'{username} изменил статус задачи {name_or_data("task", "task")} с {self.data.get("old")} на {self.data.get("new")}',
            'team_changed_priority': lambda: f'{username} изменил приоритет задачи {name_or_data("task", "task")} с {self.data.get("old")} на {self.data.get("new")}',
            'task_executor_changed': lambda: f'За задачу {name_or_data("task", "task")} назначены исполнители {self.data.get("data")}',
            'task_no_executor': lambda: f'У задачи {name_or_data("task", "task")} больше нет исполнителей',
            'tag_created': lambda: f'{username} создал новый тег {self.data.get("data")}',
            'tag_deleted': lambda: f'{username} удалил тег {self.data.get("data")}',
            'task_tag_changed': lambda: f'{username} в задаче {name_or_data("task", "task")} изменил теги: {self.data.get("data")}',
            'status_created': lambda: f'{username} создал новый статус {self.data.get("data")}',
            'status_deleted': lambda: f'{username} удалил статус {self.data.get("data")}',
            'comment_created': lambda: f'{username} оставил комментарий к задаче {name_or_data("task", "task")}: {self.data.get("data")}',
            'comment_deleted': lambda: f'{username} удалил комментарий к задаче {name_or_data("task", "task")}',
        }

        return actions.get(self.action_type, lambda: 'Неизвестное действие')()

        # if self.action_type == 'team_deleted':
        #     string = f'Команда {self.team.name if self.project else self.data.get('team_name')} была удалена'
        #     return string
        # if self.action_type == 'team_changed_name':
        #     string = f'Пользователь {username} изменил название команды {self.data.get('old')} на {self.data.get('new')}'
        #     return string
        # if self.action_type == 'team_changed_description':
        #     string = f'Пользователь {username} изменил описание команды {self.team.name if self.project else self.data.get('team_name')} с {self.data.get('old')} на {self.data.get('new')}'
        #     return string
        # 
        # if self.action_type == 'team_changed_photo':
        #     string = f'Пользователь {username} изменил фото команды {self.team.name if self.project else self.data.get('team_name')}'
        #     return string

        # if self.action_type == 'team_member_joined':
        #     string = f'Пользователь {username} вступил в команду {self.team.name if self.project else self.data.get('team_name')}'
        #     return string

        # if self.action_type == 'team_member_role_changed':
        #     string = f'У {username} была сменена роль с {self.data.get('old')} на {self.data.get('new')}'
        #     return string

        # if self.action_type == 'team_member_left':
        #     string = f'Пользователь {username} покинул команду {self.team.name if self.project else self.data.get('team_name')}'
        #     return string

        # if self.action_type == 'project_created':
        #     string = f'{username} создал проект {self.project.name if self.project else self.data.get('project_name')}'
        #     return string

        # if self.action_type == 'project_changed_name':
        #     string = f'{username} изменил имя проекта "{self.data.get('old')}" на "{self.data.get('new')}"'
        #     return string

        # if self.action_type == 'project_changed_description':
        #     string = f'{username} изменил описание проекта "{self.data.get('old')}" на "{self.data.get('new')}"'
        #     return string

        # if self.action_type == 'project_changed_photo':
        #     string = f'{username} изменил фото проекта {self.project.name if self.project else self.data.get('project_name')}'
        #     return string
        
        # if self.action_type == 'project_changed_status':
        #     string = f'{username} изменил статус проекта {self.project.name if self.project else self.data.get('project_name')} с "{self.data.get('old')}" на "{self.data.get('new')}"'
        #     return string
        
        # if self.action_type == 'project_deleted':
        #     string = f'{username} удалил проект {self.project.name if self.project else self.data.get('project_name')}'
        #     return string

        # if self.action_type == 'task_created':
        #     string = f'{username} создал задачу {self.task.name if self.task else self.data.get('task_name')}'
        #     return string
        
        # if self.action_type == 'subtask_created':
        #     string = f'{username} создал подзадачу {self.task.name if self.task else self.data.get('task_name')}'
        #     return string
        
        # if self.action_type == 'task_deleted':
        #     string = f'{username} удалил задачу {self.task.name if self.task else self.data.get('task_name')}'
        #     return string

        # if self.action_type == 'team_changed_name':
        #     string = f'{username} изменил имя задачи с {self.data.get('old')} на {self.data.get('new')}'
        #     return string
        
        # if self.action_type == 'team_changed_description':
        #     string = f'{username} изменил описание задачи {self.task.name if self.task else self.data.get('task_name')} с {self.data.get('old')} на {self.data.get('new')}'
        #     return string
        
        # if self.action_type == 'team_changed_status':
        #     string = f'{username} изменил статус задачи {self.task.name if self.task else self.data.get('task_name')} с {self.data.get('old')} на {self.data.get('new')}'
        #     return string
        
        # if self.action_type == 'team_changed_priority':
        #     string = f'{username} изменил приоритет задачи {self.task.name if self.task else self.data.get('task_name')} с {self.data.get('old')} на {self.data.get('new')}'
        #     return string

        # if self.action_type == 'task_executor_changed':
        #     string = f'За задачу {self.task.name if self.task else self.data.get('task_name')} назначены исполнители {self.data.get('data')}'
        #     return string

        # if self.action_type == 'task_no_executor':
        #     string = f'У задачи {self.task.name if self.task else self.data.get('task_name')} больше нет исполнителей'
        #     return string

        # if self.action_type == 'tag_created':
        #     string = f'{username} создал новый тег {self.data.get('data')}'
        #     return string

        # if self.action_type == 'tag_deleted':
        #     string = f'{username} удалил тег {self.data.get('data')}'
        #     return string

        # if self.action_type == 'task_tag_changed':
        #     string = f'{username} в задаче {self.task.name if self.task else self.data.get('task_name')} изменил теги: {self.data.get('data')}'
        #     return string

        # if self.action_type == 'status_created':
        #     string = f'{username} создал новый статус {self.data.get('data')}'
        #     return string

        # if self.action_type == 'status_deleted':
        #     string = f'{username} удалил статус {self.data.get('data')}'
        #     return string

        # if self.action_type == 'comment_created':
        #     string = f'{username} оставил комментарие к задаче {self.task.name if self.task else self.data.get('task_name')}: {self.data.get('data')}'
        #     return string

        # if self.action_type == 'comment_deleted':
        #     string = f'{username} удалил комментарий к задаче {self.task.name if self.task else self.data.get('task_name')}'
        #     return string

    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'История действия'
        verbose_name_plural = 'История действий'