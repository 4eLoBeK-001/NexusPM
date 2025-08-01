from django.db.models.signals import post_save
from django.dispatch import receiver
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