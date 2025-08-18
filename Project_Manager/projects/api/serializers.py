from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404
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



class AddMemberProjectSerializer(serializers.Serializer):
    logins = serializers.CharField()

    def validate(self, data):
        logins = data['logins']
        list_of_logins = [login.strip() for login in logins.split(',')]
        found_list = []
        not_found_list = []

        project_id = self.context.get('view').kwargs.get('project_id')
        project = get_object_or_404(Project, pk=project_id)

        for login in list_of_logins:
            try:
                user = User.objects.get(username=login)
                if project.project_members.filter(id=user.id).exists():
                    not_found_list.append(login)
                else:
                    found_list.append(user)
            except:
                not_found_list.append(login)

        data['found_list'] = found_list
        data['not_found_list'] = not_found_list
        return data

    

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
