from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver

from teams.middleware import get_current_user

from .models import Task, Tag, Status, TaskImage, Comment
from users.models import TaskExecutor


@receiver(signal=post_save, sender=Task)
def create_task_signal(sender, instance, created, *args, **kwargs):
    if created:
        if instance.parent_task:
            print(f'Команда - {instance.project.team.name} \n'
                  f'Проект - {instance.project.name} \n'
                  f'{get_current_user()} создал подзадачу {instance.name} к задаче {instance.parent_task.name}'
                  )
        else:
            print(f'Команда - {instance.project.team.name} \n'
                  f'Проект - {instance.project.name} \n'
                  f'{get_current_user()} создал задачу {instance.name}'
            )


@receiver(signal=post_delete, sender=Task)
def delete_task_signal(sender, instance, *args, **kwargs):
    print(f'Команда - {instance.project.team.name} \n'
            f'Проект - {instance.project.name} \n'
            f'{get_current_user()} удалил задачу {instance.name}'

    )


@receiver(signal=pre_save, sender=Task)
def change_task_signal(sender, instance, *args, **kwargs):
    if not instance.pk:
        return

    user = get_current_user()
    old_instance = Task.objects.get(pk=instance.pk)

    changes = {}

    if old_instance.name != instance.name:
        changes['name'] = (old_instance.name, instance.name)
    if old_instance.description != instance.description:
        changes['description'] = (old_instance.description, instance.description)
    if old_instance.status != instance.status:
        changes['status'] = (old_instance.status, instance.status)
    if old_instance.priority != instance.priority:
        changes['priority'] = (old_instance.priority, instance.priority)


    if changes:
        if changes.get('name'):
            print(f'{user} изменил имя задачи с {old_instance.name} на {instance.name}')
        if changes.get('description'):
            print(f'{user} изменил описание задачи {instance.name} с {old_instance.description} на {instance.description}')
        if changes.get('status'):
            print(f'{user} изменил статус задачи {instance.name} с {old_instance.status} на {instance.status}')
        if changes.get('priority'):
            print(f'{user} изменил приоритет задачи {instance.name} с {old_instance.priority} на {instance.priority}')


@receiver(signal=m2m_changed, sender=Task.executor.through)
def change_executor_signal(sender, instance, action, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        executors = [executor.username for executor in instance.executor.all()]
        if executors:
            response = f'За задачу {instance.name} назначены исполнители: \n{', '.join(executors)}'
        else:
            response = f'У задачи {instance.name} больше нет исполнителей'
        print(response)


@receiver(signal=post_save, sender=Tag)
def create_tag_signal(sender, instance, created, *args, **kwargs):
    if created:
        print(f'Команда - {instance.project.team.name} \n' 
              f'Проект - {instance.project.name} \n' 
              f'{get_current_user()} создал новый тег {instance.name}'
        )


@receiver(signal=m2m_changed, sender=Task.tag.through)
def change_tag_signal(sender, instance, action, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        
        tags_list = [tag.name for tag in instance.tag.all()]
        print(f'Пользователь {get_current_user()} в задаче {instance.name} \n'
              f'Изменил теги: {', '.join(tags_list)}'
        )


@receiver(signal=post_delete, sender=Tag)
def delete_tag_signal(sender, instance, *args, **kwargs):
    print(f'Команда - {instance.project.team.name} \n' 
            f'Проект - {instance.project.name} \n' 
            f'{get_current_user()} удалил тег {instance.name}'
    )


@receiver(signal=post_save, sender=Status)
def create_status_signal(sender, instance, created, *args, **kwargs):
    if created:
        print(f'Команда - {instance.project.team.name} \n' 
              f'Проект - {instance.project.name} \n' 
              f'{get_current_user()} создал новый статус {instance.name}'
        )


@receiver(signal=post_delete, sender=Status)
def delete_status_signal(sender, instance, *args, **kwargs):
    print(f'Команда - {instance.project.team.name} \n' 
            f'Проект - {instance.project.name} \n' 
            f'{get_current_user()} удалил статус {instance.name}'
    )


@receiver(signal=post_save, sender=Comment)
def create_comment_tag(sender, instance, created, *args, **kwargs):
    if created:
        print(f'{get_current_user()} \n'
              f'оставил комментарий к задаче {instance.task.name}: {instance.content}'
        )


@receiver(signal=post_delete, sender=Comment)
def create_comment_tag(sender, instance, *args, **kwargs):
        print(f'Задача - {instance.task.name} \n'
              f'{get_current_user()} удалил комментарий: {instance.content}'
        )
