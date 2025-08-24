from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Team
from teams.middleware import get_current_user
from users.models import TeamMember, User
from logs.services import log_action


@receiver([post_save, post_delete], sender=Team)
def invalidate_team_members_cache(sender, instance, **kwargs):
    cache.delete_pattern('teams_list_hash_*')


@receiver([post_save, post_delete], sender=TeamMember)
def invalidate_team_members_cache(sender, instance, **kwargs):
    team_id = instance.team_id
    cache.delete(f'team_{team_id}_members')


@receiver(signal=post_save, sender=Team)
def create_team_signal(sender, instance, created, *args, **kwargs):
    if created:
        TeamMember.objects.create(
            user=instance.author,
            team=instance,
            role='Creator'
        )


@receiver(signal=pre_save, sender=Team)
def change_team_signal(sender, instance, *args, **kwargs):

    if not instance.pk:
        return

    try:
        old_instance = Team.objects.get(pk=instance.pk)
        user=get_current_user()
    except Team.DoesNotExist:
        return

    changes = {}

    if old_instance.name != instance.name:
        changes['name'] = (old_instance.name, instance.name)
    if old_instance.description != instance.description:
        changes['description'] = (old_instance.description, instance.description)
    if old_instance.image != instance.image:
        changes['photo'] = 'Фото было изменено'

    if changes:
        if changes.get('name'):
            log_action(action='team_changed_name', team=instance, user=user,
                       data={'old': changes.get('name')[0], 'new': changes.get('name')[1], 'team_name': instance.name}
            )
        if changes.get('description'):
            log_action(action='team_changed_description', team=instance, user=user,
                       data={'old': changes.get('description')[0], 'new': changes.get('description')[1], 'team_name': instance.name}
            )
        if changes.get('photo'):
            log_action(action='team_changed_photo', team=instance, user=user, data={'team_name': instance.name})


@receiver(signal=pre_save, sender=TeamMember)
def team_member_joined_signal(sender, instance, *args, **kwargs):
    user = instance.user
    team = instance.team
    if not instance.pk:
        log_action(action='team_member_joined', user=user, team=team, data={'team_name': instance.team.name})
        return
    try:
        old_member = TeamMember.objects.get(pk=instance.pk)
    except TeamMember.DoesNotExist:
        return
    
    if old_member.role != instance.role:
        log_action(action='team_member_role_changed', user=user, team=team,
                   data={'old': old_member.get_role_display(),'new': instance.get_role_display(), 'team_name': instance.team.name}
        )


@receiver(signal=pre_delete, sender=TeamMember)
def team_member_left_signal(sender, instance, *args, **kwargs):
    user = instance.user
    team = instance.team
    log_action(action='team_member_left', user=user, team=team, data={'team_name': instance.team.name})


@receiver(signal=pre_delete, sender=Team)
def team_deleted_signal(sender, instance, *args, **kwargs):
    user = instance.author
    team = instance
    log_action(action='team_deleted', user=user, team=team, data={'team_name': instance.name})