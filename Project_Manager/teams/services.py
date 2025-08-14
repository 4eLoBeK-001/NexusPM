from django.shortcuts import get_object_or_404, render
from django.db.models import Q, F, Sum, Count

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



def change_member_role(request, pk, member_pk, new_role=None, *args, **kwargs):
    team = get_object_or_404(Team, pk=pk, team_member=request.user)
    member = team.participate_in_team.get(user_id=member_pk)
    if new_role is None:
        selected_role = request.POST.get('selected_role')
    else:
        selected_role = new_role
    member.role = selected_role
    member.save()
    # С аннотацией получаем дополнительно поля: 
    # projects_count - в скольких проектах участвует каждый участник
    # member_date_joining - когда присоединился
    team_member = team.team_member.annotate(
        projects_count=Count('project_membership', filter=Q(project_membership__team=team)),
        member_date_joining=F('members_teams__date_joining')
    ).get(pk=member.user.pk)
    context = {
        'team': team,
        'member': team_member,
    }
    print(context)
    return context