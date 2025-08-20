from django.shortcuts import get_object_or_404

from rest_framework import permissions

from projects.models import Project


class HasProjectMember(permissions.BasePermission):
    def has_permission(self, request, view):

        if not hasattr(view, '_cached_project'):
            try:
                view._cached_project = get_object_or_404(
                    Project, id=view.kwargs.get('project_id')
                )
            except Project.DoesNotExist:
                return False

        project = view._cached_project

        if not hasattr(view, '_cached_project_member'):
            view._cached_project_member = project.project_members.filter(
                id=request.user.id
            ).exists()

        return view._cached_project_member
