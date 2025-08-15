from rest_framework.views import APIView
from rest_framework import generics, permissions

from projects.api.serializers import ProjectsListSerializer
from projects.models import Project

class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsListSerializer