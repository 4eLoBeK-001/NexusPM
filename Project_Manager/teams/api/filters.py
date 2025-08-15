import django_filters

from teams.models import Team

class TeamFilter(django_filters.FilterSet):

    class Meta:
        model = Team
        fields = {
            'id': ['exact', 'lt', 'gt', 'range'],
            'name': ['icontains'],
            'author__username': ['icontains']
        }
