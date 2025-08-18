from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from tasks.models import Status, Tag
from users.models import ProjectMember, User
from users.api.serializers import UserSerializer
from teams.api.permissions import HasTeamRole
from teams.models import Team
from projects.api.serializers import ProjectStatusesSerializer, ProjectTagsSerializer, ProjectsDetailSerializer, ProjectsListSerializer, ProjectsMembersSerializer
from projects.models import Project

class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsListSerializer
    required_role = 'Admin'

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), HasTeamRole()]
        return [IsAuthenticated()]

    def get_team(self):
        if not hasattr(self, '_team'):
            team_id = self.kwargs.get('pk')
            team = get_object_or_404(Team, pk=team_id)
            user = self.request.user
            # Если юзер в команде то возвращаем проекты
            if not team.team_member.filter(pk=user.pk).exists():
                raise Http404("Команда не найдена")
            self._team = team
        return self._team

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['team'] = self.get_team()
        return context

    def perform_create(self, serializer):
        project = serializer.save(team=self.get_team())
        project.project_members.add(self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        team = self.get_team()
        if not team.team_member.filter(pk=self.request.user.pk).exists():
            raise Http404("Команда не найдена")
        return qs.filter(team=team, project_members=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        team = self.get_team()
        response.data = {
            'team': team.name,
            'projects': response.data
        }
        return response


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsDetailSerializer
    required_role = 'Admin'
    # Кастомный метод проверки того, в команде ли участник
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAuthenticated(), HasTeamRole()]

    def get_object(self):
        project_id = self.kwargs.get('project_id')
        return get_object_or_404(Project, id=project_id)


class ProjectMembersAPIView(generics.ListAPIView):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectsMembersSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(project_id=self.kwargs.get('project_id'))
    
    def list(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
        response = super().list(request, *args, **kwargs)
        response.data = {
            'project': {'project_id': project.id, 'project_name': project.name},
            'members': response.data
        }
        return response



class ProjectStatusesAPIView(generics.ListAPIView):
    queryset = Status.objects.all()
    serializer_class = ProjectStatusesSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(project_id=self.kwargs.get('project_id'))
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
        response.data = {
            'project': {'project_id': project.id, 'project_name': project.name},
            'statuses': response.data
        }
        return response


class ProjectTagsAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = ProjectTagsSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(project_id=self.kwargs.get('project_id'))
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
        response.data = {
            'project': {'project_id': project.id, 'project_name': project.name},
            'tags': response.data
        }
        return response