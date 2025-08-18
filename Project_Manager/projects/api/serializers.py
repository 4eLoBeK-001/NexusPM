from rest_framework import serializers

from tasks.models import Status, Tag
from users.api.serializers import UserSerializer
from projects.models import Project
from users.models import ProjectMember, User


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


class ProjectsMembersSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProjectMember
        fields = ('user', 'date_joining')


class ProjectStatusesSerializer(serializers.ModelSerializer):
    color_name = serializers.CharField(source='color.name')

    class Meta:
        model = Status
        fields = ('name', 'color_name', 'is_completed')



class ProjectTagsSerializer(serializers.ModelSerializer):
    color_name = serializers.CharField(source='color.name')

    class Meta:
        model = Tag
        fields = ('name', 'color_name')