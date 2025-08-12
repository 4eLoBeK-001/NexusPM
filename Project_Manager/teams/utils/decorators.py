from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from users.models import TeamMember

# Декоратор ограничивает различные действия, 
# если переданная роль min_role_required ниже по приоритету чем роль участника
def role_required(min_role_required):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            team_pk = kwargs.get('pk')
            if team_pk is None:
                raise ValueError('Team (ID) не передан в функцию, его наличие обязательно')

            team_member = get_object_or_404(TeamMember, team_id=team_pk, user=request.user)
            required_role = TeamMember.RoleChoices.get_priority(min_role_required)
            role_proirty = team_member.RoleChoices.get_priority(team_member.role)

            if required_role > role_proirty:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator