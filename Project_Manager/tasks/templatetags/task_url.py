from django import template

from django.urls import reverse

register = template.Library()

@register.simple_tag
def url_task(task, action_name):
    return reverse(
        f'teams:projects:tasks:{action_name}',
        args=[task.project.team.pk, task.project.pk, task.pk]
    )