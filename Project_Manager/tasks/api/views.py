from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from teams.api.permissions import HasTeamRole

from projects.api.permissions import HasProjectMember
from projects.models import Project

from tasks.api.serializers import CommentSerializer, TaskDetailSerializer, TaskListSerializer
from tasks.models import Comment, Task


class TaskListAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all().select_related('status__color', 'parent_task').prefetch_related('tag__color', 'executor__profile')
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


class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    required_role = 'Viewer'

    def perform_create(self, serializer):
        task = get_object_or_404(Task, pk=self.kwargs.get('task_id'))
        serializer.save(author=self.request.user, task=task)

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [HasProjectMember(), HasTeamRole()]
        return [HasProjectMember()]
        
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        task = get_object_or_404(Task, pk=self.kwargs.get('task_id'))
        response.data = {
            'task': {'task_id': task.id, 'task_name': task.name},
            'comments': response.data
        }
        return response


class CommentDeleteAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [HasTeamRole, HasProjectMember]
    required_role = 'Manager'
    lookup_url_kwarg = 'comment_id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'detail': 'Комментарий успешно удалён'}
        )