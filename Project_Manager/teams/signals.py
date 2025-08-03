from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import Team
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
def pre_signal(sender, instance, *args, **kwargs):
    old_instance = get_object_or_404(Team, pk=instance.id)


    if old_instance.name != instance.name:
        print('Изменено имя')
    if old_instance.description != instance.description:
        print('Изменено описание')
    if old_instance.image != instance.image:
        print('Изменено фото')


@receiver(signal=post_save, sender=Team)
def signal_notif(sender, instance, created, *args, **kwargs):
    ...