from rest_framework import serializers

from projects.api.serializers import ProjectStatusesSerializer, ProjectTagsSerializer
from tasks.models import Status, Tag, Task
from users.api.serializers import UserSerializer


class TaskListSerializer(serializers.ModelSerializer):
    executor = UserSerializer(many=True, read_only=True)
    status = serializers.CharField(source='status.name', read_only=True)
    tag = ProjectTagsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ('id', 'name', 'executor', 'status', 'tag', 'priority')


class TaskDetailSerializer(serializers.ModelSerializer):
    executor = UserSerializer(many=True, read_only=True)

    # для чтения
    status_display = serializers.CharField(source='status.name', read_only=True)
    tag_display = ProjectTagsSerializer(source='tag', many=True, read_only=True)

    # для записи
    status = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(),
        write_only=True, required=False, allow_null=True
    )
    tag = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True, write_only=True, required=False
    )

    class Meta:
        model = Task
        fields = (
            'id', 'name', 'description', 'color', 'creator', 'project',
            'status', 'status_display', 'tag', 'tag_display',
            'priority', 'created_at', 'updated_at', 'parent_task', 'executor'
        )
        read_only_fields = (
            'color', 'creator', 'project',
            'created_at', 'updated_at',
            'parent_task', 'executor'
        )
