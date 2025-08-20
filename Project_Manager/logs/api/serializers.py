from rest_framework import serializers

from logs.models import ActionLog

class LogActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionLog
        fields = ('user', 'team', 'project', 'task', 'action_type', 'data', 'created_at', 'participants')