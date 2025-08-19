import django_filters
from django.db.models import F

from users.models import ProjectMember
from projects.models import Project


class ProjectFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(method='filter_by_username')

    class Meta:
        model = Project
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
        }

    def filter_by_username(self, queryset, name, value):
        return queryset.filter(
            project_members__username__icontains=value
        )


class ProjectMemberFilter(django_filters.FilterSet):
    class Meta:
        model = ProjectMember
        fields = {
            'user__username': ['icontains'],
        }