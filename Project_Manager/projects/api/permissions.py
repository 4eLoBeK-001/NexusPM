from django.shortcuts import get_object_or_404

from rest_framework import permissions

from projects.models import Project


class HasProjectMember(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs.get('project_id'))

        if request.user in project.project_members.all():
            return True
        return False

