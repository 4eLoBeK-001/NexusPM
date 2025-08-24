import hashlib
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from projects.api.filters import ProjectFilter, ProjectMemberFilter
from projects.api.permissions import HasProjectMember
from tasks.models import Status, Tag
from users.models import ProjectMember, User
from users.api.serializers import UserSerializer
from teams.api.permissions import HasTeamRole
from teams.models import Team
from projects.api.serializers import AddMemberProjectSerializer, ProjectStatusesSerializer, ProjectTagsSerializer, ProjectsDetailSerializer, ProjectsListSerializer, ProjectsMembersSerializer
from projects.models import Project

class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsListSerializer
    filterset_class = ProjectFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        
    ]
    ordering_fields = ['-created_at']
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
        return qs.filter(team=team, project_members=self.request.user).prefetch_related('project_members__profile')

    def list(self, request, *args, **kwargs):
        team = self.get_team()

        # Если запрос с параметрами то ничего не кэшируем
        if request.query_params:
            return super().list(request, *args, **kwargs)

        user = request.user
        project_ids = list(Project.objects.filter(team=team, project_members=user).values_list("id", flat=True))
        project_ids.sort()
        projects_hash = hashlib.md5(str(project_ids).encode()).hexdigest()

        cache_key = f'projects_list_hash_{projects_hash}'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        response.data = {
            'team': team.name,
            'projects': response.data
        }
        cache.set(cache_key, response.data, timeout=60*60)
        return response


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsDetailSerializer
    required_role = 'Admin'

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAuthenticated(), HasTeamRole()]

    def get_object(self):
        project_id = self.kwargs.get('project_id')
        return get_object_or_404(Project.objects.prefetch_related('project_members__profile'), id=project_id)


class ProjectMembersAPIView(generics.ListCreateAPIView):
    queryset = ProjectMember.objects.all()
    permission_classes = [HasProjectMember]
    filterset_class = ProjectMemberFilter
    filter_backends = [
        DjangoFilterBackend,
    ]
    required_role = 'Admin'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'view': self})
        serializer.is_valid(raise_exception=True)

        added_users, not_found_logins = serializer.save()

        return Response({
            'added': [user.username for user in added_users],
            'not_found': not_found_logins
        }, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [HasProjectMember(), HasTeamRole()]
        return [HasProjectMember()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddMemberProjectSerializer
        return ProjectsMembersSerializer

    def get_queryset(self):
        return super().get_queryset().filter(project_id=self.kwargs['project_id']).select_related('user').prefetch_related('user__profile')
    
    def list(self, request, *args, **kwargs):
        project = self._get_project()
        response = super().list(request, *args, **kwargs)
        response.data = {
            'project': {'project_id': project.id, 'project_name': project.name},
            'members': response.data
        }
        return response
    
    def _get_project(self):
        """Получить проект по ID из URL параметров"""
        project_id = self.kwargs.get('project_id')
        return get_object_or_404(Project, id=project_id)


class ProjectStatusesAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all().select_related('color', 'project')
    serializer_class = ProjectStatusesSerializer
    required_role = 'Manager'

    def get_permissions(self):
        if self.request.method == 'POST':
            return [HasProjectMember(), HasTeamRole()]
        return [HasProjectMember()]
    
    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
        serializer.save(project=project)

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


class ProjectTagsAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all().select_related('color', 'project')
    serializer_class = ProjectTagsSerializer
    permission_classes = [HasProjectMember]
    required_role = 'Member'

    def get_permissions(self):
        if self.request.method == 'POST':
            return [HasProjectMember(), HasTeamRole()]
        return [HasProjectMember()]
    
    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
        serializer.save(project=project)

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