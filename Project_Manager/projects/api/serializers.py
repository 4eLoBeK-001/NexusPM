from rest_framework import serializers

from tasks.models import Color, Status, Tag
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
        read_only_fields = ('date_joining',)


class ProjectStatusesSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source='color.color_name')

    class Meta:
        model = Status
        fields = ('name', 'color', 'is_completed')

    def create(self, validated_data):
        color_name = validated_data.pop('color')['color_name']
        color = Color.objects.get(name=color_name)
        return Status.objects.create(color=color, **validated_data)


class ProjectTagsSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source='color.color_name')

    class Meta:
        model = Tag
        fields = ('name', 'color')
    
    def create(self, validated_data):
        color_name = validated_data.pop('color')['color_name']
        color = Color.objects.get(name=color_name)
        return Tag.objects.create(color=color, **validated_data)
