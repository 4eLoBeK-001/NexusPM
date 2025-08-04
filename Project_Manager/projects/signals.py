from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

from teams.middleware import get_current_user

from .models import Project

from logs.services import log_action


@receiver(signal=post_save, sender=Project)
def create_project_signal(sender, instance, created, *args, **kwargs):
    if created:
        log_action(action='project_created', user=get_current_user(), team=instance.team, project=instance)



@receiver(signal=pre_save, sender=Project)
def change_project_signal(sender, instance, *args, **kwargs):
    if not instance.pk:
        return

    old_instance = Project.objects.get(pk=instance.pk)
    
    changes = {}

    if old_instance.name != instance.name:
        changes['name'] = (old_instance.name, instance.name)
    if old_instance.description != instance.description:
        changes['description'] = (old_instance.description, instance.description)
    if str(old_instance.image) != str(instance.image):
        changes['photo'] = 'Фото было изменено'
    if old_instance.status != instance.status:
        changes['status'] = (old_instance.status, instance.status)

    
    if changes:
        if changes.get('name'):
            log_action(action='project_changed_name', user=get_current_user(), project=instance, data={'old': changes.get('name')[0], 'new': changes.get('name')[1]})
        if changes.get('description'):
            log_action(action='project_changed_description', user=get_current_user(), project=instance, data={'old': changes.get('description')[0], 'new': changes.get('description')[1]})
        if changes.get('photo'):
            log_action(action='project_changed_photo', user=get_current_user(), project=instance)
        if changes.get('status'):
            log_action(action='project_changed_status', user=get_current_user(), project=instance, data={'old': changes.get('status')[0], 'new': changes.get('status')[1]})


@receiver(signal=pre_delete, sender=Project)
def delete_project_signal(sender, instance, origin, *args, **kwargs):
    print(instance.description)
    log_action(action='project_deleted', user=get_current_user(), team=instance.team, project=instance)
