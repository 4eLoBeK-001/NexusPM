from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from logs.api.filters import LogsFilter
from logs.api.serializers import LogActionsSerializer
from logs.models import ActionLog

from teams.models import Team
from projects.models import Project


class LogActionsAPIView(generics.ListAPIView):
    queryset = ActionLog.objects.all()
    serializer_class = LogActionsSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = LogsFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            participants=self.request.user
        ).select_related(
            'user', 'team', 'project', 'task'
        ).prefetch_related(
            'participants'
        ).distinct().order_by('-created_at')
        return qs


class TeamHistoryAPIView(generics.ListAPIView):
    queryset = ActionLog.objects.all()
    serializer_class = LogActionsSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = LogsFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        team = get_object_or_404(Team, pk=self.kwargs.get('pk'))
        return qs.filter(participants=self.request.user, team=team).select_related(
            'user', 'team', 'project', 'task'
        ).prefetch_related(
            'participants'
        )


class ProjectHistoryAPIView(generics.ListAPIView):
    queryset = ActionLog.objects.all()
    serializer_class = LogActionsSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = LogsFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        project = get_object_or_404(Project, pk=self.kwargs.get('project_id'))
        return qs.filter(participants=self.request.user, project=project).select_related(
            'user', 'team', 'project', 'task'
        ).prefetch_related(
            'participants'
        )
