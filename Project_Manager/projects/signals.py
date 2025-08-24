from django.db.models.signals import post_save, pre_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.cache import cache
from teams.middleware import get_current_user

from .models import Project

from users.models import ProjectMember

from tasks.models import Status

from logs.services import log_action

@receiver((post_delete, post_save), sender=Project)
def invalidate_project_cache(sender, instance, **kwargs):
    cache_key = 'projects_list_hash_*'
    cache.delete_pattern(cache_key)


@receiver(m2m_changed, sender=Project.project_members.through)
def invalidate_project_members_cache(sender, instance, **kwargs):
    cache_key = f'project_{instance.id}_members'
    cache.delete(cache_key)


@receiver(signal=post_save, sender=Project)
def create_project_signal(sender, instance, created, *args, **kwargs):
    if created:
        log_action(action='project_created', user=get_current_user(), team=instance.team, project=instance, data={'project_name': instance.name})
        Status.objects.create(project=instance, name='Новая', color_id=3)
        Status.objects.create(project=instance, name='Завершена', is_completed=True, color_id=1)


@receiver(signal=pre_save, sender=Project)
def change_project_signal(sender, instance, *args, **kwargs):
    if not instance.pk:
        return

    old_instance = Project.objects.get(pk=instance.pk)
    user = get_current_user()

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
            log_action(action='project_changed_name', user=user, project=instance, data={'old': changes.get('name')[0], 'new': changes.get('name')[1], 'project_name': instance.name, 'team_name': instance.team.name})
        if changes.get('description'):
            log_action(action='project_changed_description', user=user, project=instance, data={'old': changes.get('description')[0], 'new': changes.get('description')[1], 'project_name': instance.name, 'team_name': instance.team.name})
        if changes.get('photo'):
            log_action(action='project_changed_photo', user=user, project=instance, data={'project_name': instance.name, 'team_name': instance.team.name})
        if changes.get('status'):
            log_action(action='project_changed_status', user=user, project=instance, data={'old': changes.get('status')[0], 'new': changes.get('status')[1], 'project_name': instance.name, 'team_name': instance.team.name})


@receiver(signal=pre_delete, sender=Project)
def delete_project_signal(sender, instance, origin, *args, **kwargs):
    log_action(action='project_deleted', user=get_current_user(), team=instance.team, project=instance, data={'project_name': instance.name, 'team_name': instance.team.name})
