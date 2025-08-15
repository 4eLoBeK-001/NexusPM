from django.shortcuts import get_object_or_404

from rest_framework import permissions

from users.models import TeamMember


class HasTeamRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
    
        min_role = getattr(view, 'required_role')
        if not min_role:
            return True

        team_pk = view.kwargs.get('pk')
        if not team_pk:
            return False
        
        my_role = get_object_or_404(TeamMember, user=request.user, team_id=team_pk).role
        
        if TeamMember.RoleChoices.get_priority(my_role) >= TeamMember.RoleChoices.get_priority(min_role):
            return True
        return False