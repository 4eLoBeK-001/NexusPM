from django.shortcuts import get_object_or_404
from rest_framework import generics

from teams.api.permissions import HasTeamRole

from projects.api.permissions import HasProjectMember
from projects.models import Project

from tasks.api.serializers import TaskDetailSerializer, TaskListSerializer
from tasks.models import Task


class TaskListAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    required_role = 'Member'

    def get_permissions(self):
        if self.request.method == 'POST':
            return [HasProjectMember(), HasTeamRole()]
        return [HasProjectMember()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        project = get_object_or_404(Project, pk=kwargs.get('project_id'))
        response.data = {
            'project': {'project_id': project.id, 'project_name': project.name},
            'tasks': response.data
        }
        return response


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_url_kwarg = 'task_id'

    method_required_roles = {
        'DELETE': 'Manager',
        'PUT': 'Member',
        'PATCH': 'Member',
    }

    def get_required_role(self):
        return self.method_required_roles.get(self.request.method, 'Member')

    def get_permissions(self):
        self.required_role = self.get_required_role()

        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [HasProjectMember(), HasTeamRole()]
        return [HasProjectMember()]