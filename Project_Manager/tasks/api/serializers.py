from rest_framework import serializers

from projects.api.serializers import ProjectStatusesSerializer, ProjectTagsSerializer
from tasks.models import Task
from users.api.serializers import UserSerializer


class TaskListSerializer(serializers.ModelSerializer):
    executor = UserSerializer(many=True, read_only=True)
    status = serializers.CharField(source='status.name', read_only=True)
    tag = ProjectTagsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ('id', 'name', 'executor', 'status', 'tag', 'priority')