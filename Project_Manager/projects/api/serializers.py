from rest_framework import serializers

from projects.models import Project
from users.models import User


class ProjectsListSerializer(serializers.ModelSerializer):
    class Meta:
        # Добавить человеческой отображение project_members, вместо айдишников
        model = Project
        fields = ('id', 'name', 'status', 'project_members')