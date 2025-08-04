from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete, pre_delete
from django.dispatch import receiver

from teams.middleware import get_current_user

from .models import Task, Tag, Status, TaskImage, Comment

from users.models import TaskExecutor

from logs.services import log_action


@receiver(signal=post_save, sender=Task)
def create_task_signal(sender, instance, created, *args, **kwargs):
    if created:
        if instance.parent_task:
            log_action(action='subtask_created', user=get_current_user(), task=instance, data={'task_name': instance.name})

        else:
            log_action(action='task_created', user=get_current_user(), task=instance, data={'task_name': instance.name})



@receiver(signal=pre_delete, sender=Task)
def delete_task_signal(sender, instance, *args, **kwargs):
    log_action(action='task_deleted', user=get_current_user(), task=instance, data={'task_name': instance.name})



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
            log_action(action='team_changed_name', user=get_current_user(), task=instance, data={'old': old_instance.name, 'new': instance.name, 'task_name': instance.name})
        if changes.get('description'):
            log_action(action='team_changed_description', user=get_current_user(), task=instance, data={'old': old_instance.description, 'new': instance.description, 'task_name': instance.name})
        if changes.get('status'):
            print(f'{user} изменил статус задачи {instance.name} с {old_instance.status} на {instance.status}')
            log_action(action='team_changed_status', user=get_current_user(), task=instance, data={'old': str(changes.get('status')[0]), 'new': str(changes.get('status')[1]), 'task_name': instance.name})
        if changes.get('priority'):
            log_action(action='team_changed_priority', user=get_current_user(), task=instance, data={'old': old_instance.priority, 'new': instance.priority, 'task_name': instance.name})


@receiver(signal=m2m_changed, sender=Task.executor.through)
def change_executor_signal(sender, instance, action, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        executors = [executor.username for executor in instance.executor.all()]
        if executors:
            log_action(action='task_executor_changed', user=get_current_user(), task=instance, data={'data': ', '.join(executors), 'task_name': instance.name})
        else:
            log_action(action='task_no_executor', user=get_current_user(), task=instance, data={'task_name': instance.name})


@receiver(signal=post_save, sender=Tag)
def create_tag_signal(sender, instance, created, *args, **kwargs):
    if created:
        log_action(action='tag_created', user=get_current_user(), project=instance.project, data={'data': instance.name, 'tag_name': instance.name})


@receiver(signal=m2m_changed, sender=Task.tag.through)
def change_tag_signal(sender, instance, action, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        
        tags_list = [tag.name for tag in instance.tag.all()]
        log_action(action='task_tag_changed', user=get_current_user(), task=instance, data={'data': ', '.join(tags_list), 'tag_name': ', '.join(tags_list)})



@receiver(signal=post_delete, sender=Tag)
def delete_tag_signal(sender, instance, *args, **kwargs):
        log_action(action='tag_deleted', user=get_current_user(), project=instance.project, data={'data': instance.name, 'tag_name': instance.name})


@receiver(signal=post_save, sender=Status)
def create_status_signal(sender, instance, created, *args, **kwargs):
    if created:
        log_action(action='status_created', user=get_current_user(), project=instance.project, data={'data': instance.name})



@receiver(signal=post_delete, sender=Status)
def delete_status_signal(sender, instance, *args, **kwargs):
    log_action(action='status_deleted', user=get_current_user(), project=instance.project, data={'data': instance.name})



@receiver(signal=post_save, sender=Comment)
def create_comment_signal(sender, instance, created, *args, **kwargs):
    if created:
        log_action(action='comment_created', user=get_current_user(), task=instance.task, data={'data': instance.content})


@receiver(signal=pre_delete, sender=Comment)
def delete_comment_signal(sender, instance, *args, **kwargs):
    log_action(action='comment_deleted', user=get_current_user(), task=instance.task, data={'data': instance.content})

