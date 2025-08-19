from django.shortcuts import get_object_or_404
from rest_framework import generics

from projects.models import Project
from tasks.api.serializers import TaskListSerializer
from tasks.models import Task


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        response.data = {
            'project': {'project_id': project.id, 'project_name': project.name},
            'tasks': response.data
        }
        return response