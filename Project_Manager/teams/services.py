from django.shortcuts import get_object_or_404, render

from .models import Team
from .utils.utils import get_role_description, ROLE_PERMISSIONS, PERMISSION_LABELS
from users.models import TeamMember



def get_team_roles(request, pk=None):
    context = {}
    # Функция формирует список словарей с информацией о каждой роли:
    # - value: значение роли в модели
    # - label: название роли для отображения
    # - rights: описание прав доступа
    # - description: описание роли
    roles = [
        {
            'value': role.value, 
            'label': role.label, 
            'rights': ROLE_PERMISSIONS[role.value], 
            'description': get_role_description(role.value)
        } 
        for role in TeamMember.RoleChoices
    ]

    context = {
        'roles': roles,
        'rights_labels': PERMISSION_LABELS
    }
    if pk is not None:
        team = get_object_or_404(Team, pk=pk, team_member=request.user)
        context.update({'team': team})

    return context