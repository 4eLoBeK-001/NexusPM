from rest_framework import serializers

from users.api.serializers import UserSerializer
from projects.models import Project
from users.models import User


class ProjectsListSerializer(serializers.ModelSerializer):
    project_members = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ('id', 'name', 'status', 'project_members')
        read_only_fields = ('status',)


class ProjectsDetailSerializer(serializers.ModelSerializer):
    project_members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'image', 'status', 'color', 'team', 'project_members', 'created_at', 'updated_at')
        read_only_fields = ('id', 'team', 'project_members', 'created_at', 'updated_at')