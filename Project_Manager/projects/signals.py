from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

from teams.middleware import get_current_user

from .models import Project


@receiver(signal=post_save, sender=Project)
def create_project_signal(sender, instance, created, *args, **kwargs):
    if created:
        print(f'Команда - {instance.team.name} \n' 
              f'{get_current_user()} создал команду {instance}'
        )


@receiver(signal=pre_save, sender=Project)
def change_project_signal(sender, instance, *args, **kwargs):
    old_instance = Project.objects.get(pk=instance.pk)
    
    changes = {}

    if old_instance.name != instance.name:
        changes['name'] = (old_instance.name, instance.name)
    if old_instance.description != instance.description:
        changes['description'] = (old_instance.description, instance.description)
    if old_instance.image != instance.image:
        changes['photo'] = 'Фото было изменено'
    if old_instance.status != instance.status:
        changes['status'] = (old_instance.status, instance.status)

    
    if changes:
        if changes.get('name'):
            print(f'Пользователь {get_current_user()} изменил имя проекта "{changes.get('name')[0]}" на "{changes.get('name')[1]}"')
        if changes.get('description'):
            print(f'Пользователь {get_current_user()} изменил описание проекта "{instance.name}" с "{changes.get('description')[0]}" на "{changes.get('description')[1]}"')
        if changes.get('photo'):
            print(f'Пользователь {get_current_user()} изменил фото проекта "{instance.name}"')
        if changes.get('status'):
            print(f'Пользователь {get_current_user()} изменил статус проекта "{instance.name}" с "{changes.get('status')[0]}" на "{changes.get('status')[1]}"')




@receiver(signal=post_delete, sender=Project)
def delete_project_signal(sender, instance, *args, **kwargs):
    print(f'{get_current_user()} удалил проект {instance}')