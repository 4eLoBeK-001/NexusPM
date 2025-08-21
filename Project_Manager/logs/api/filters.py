import django_filters

from logs.models import ActionLog

class LogsFilter(django_filters.FilterSet):
    action_type = django_filters.ChoiceFilter(
        field_name='action_type',
        choices=ActionLog.ACTION_CHOICES
    )

    class Meta:
        model = ActionLog
        fields = {
            'user__username': ['icontains']
        }
    
