from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

from teams.middleware import get_current_user

from .models import Task, Tag, Status, TaskImage, Comment


@receiver(signal=post_save, sender=Tag)
def create_tag_signal(sender, instance, created, *args, **kwargs):
    if created:
        print(f'Команда - {instance.project.team.name} \n' 
              f'Проект - {instance.project.name} \n' 
              f'{get_current_user()} создал новый тег {instance}'
        )

@receiver(signal=post_delete, sender=Tag)
def delete_tag_signal(sender, instance, *args, **kwargs):
    print(f'Команда - {instance.project.team.name} \n' 
            f'Проект - {instance.project.name} \n' 
            f'{get_current_user()} удалил тег {instance}'
    )

@receiver(signal=post_save, sender=Status)
def create_tag_signal(sender, instance, created, *args, **kwargs):
    if created:
        print(f'Команда - {instance.project.team.name} \n' 
              f'Проект - {instance.project.name} \n' 
              f'{get_current_user()} создал новый статус {instance}'
        )

@receiver(signal=post_delete, sender=Status)
def delete_tag_signal(sender, instance, *args, **kwargs):
    print(f'Команда - {instance.project.team.name} \n' 
            f'Проект - {instance.project.name} \n' 
            f'{get_current_user()} удалил статус {instance}'
    )



