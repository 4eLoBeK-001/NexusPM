import django_filters

from teams.models import Team, TeamMember

class TeamFilter(django_filters.FilterSet):

    class Meta:
        model = Team
        fields = {
            'id': ['exact', 'lt', 'gt', 'range'],
            'name': ['icontains'],
            'author__username': ['icontains']
        }


class TeamMemberFilter(django_filters.FilterSet):

    class Meta:
        model = TeamMember
        fields = {
            'user__username': ['icontains'],
            'user__email': ['icontains'],
        }
