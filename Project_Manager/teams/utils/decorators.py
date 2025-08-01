from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from users.models import TeamMember

def role_required(min_role_required):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, pk, *args, **kwargs):
            team_member = get_object_or_404(TeamMember, team_id=pk, user=request.user)
            required_role = TeamMember.RoleChoices.get_priority(min_role_required)
            role_proirty = team_member.RoleChoices.get_priority(team_member.role)

            if required_role >= role_proirty :
                raise PermissionDenied

            return view_func(request, pk, *args, **kwargs)
        return wrapper
    return decorator