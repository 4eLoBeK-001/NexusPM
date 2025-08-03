from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from .models import Team
from teams.middleware import get_current_user
from users.models import TeamMember, User


@receiver(signal=post_save, sender=Team)
def signal_create(sender, instance, created, *args, **kwargs):
    if created:
        TeamMember.objects.create(
            user=instance.author,
            team=instance,
            role='Creator'
        )

@receiver(signal=pre_save, sender=Team)
def pre_team_signal(sender, instance, *args, **kwargs):

    if not instance.pk:
        return

    try:
        old_instance = Team.objects.get(pk=instance.pk)
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
            print(f'Пользователь {get_current_user()} изменил имя команды "{changes.get('name')[0]}" на "{changes.get('name')[1]}"')
        if changes.get('description'):
            print(f'Пользователь {get_current_user()} изменил описание команды "{instance.name}" с "{changes.get('description')[0]}" на "{changes.get('description')[1]}"')
        if changes.get('photo'):
            print(f'Пользователь {get_current_user()} изменил фото команды "{instance.name}"')


@receiver(signal=pre_save, sender=TeamMember)
def team_member_joined_signal(sender, instance, *args, **kwargs):
    user = instance.user
    team = instance.team
    if not instance.pk:
        print(f'Пользователь {user.username} вступил в команду {team.name}')
        return
    try:
        old_member = TeamMember.objects.get(pk=instance.pk)
    except TeamMember.DoesNotExist:
        return

    print(
        f'У пользователя {user.username} в команде {team.name} была сменена роль '
        f'с "{old_member.get_role_display()}" на "{instance.get_role_display()}"'
    )


@receiver(signal=pre_delete, sender=TeamMember)
def team_member_left_signal(sender, instance, *args, **kwargs):
    user = instance.user
    team = instance.team
    print(f'Пользователь {user.username} покинул команду {team.name}')

