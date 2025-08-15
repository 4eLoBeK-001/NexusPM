from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from teams.api.permissions import HasTeamRole
from users.models import TeamMember
from teams.models import Team
from teams.api.serializers import TeamListSerializer, TeamDetailSerializer, TeamMemberSerializer
from teams.services import get_team_roles, change_member_role


class TeamListCreateAPIView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(team_member=user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response['X-Header'] = 'Creating and listing teams'
        return response


class TeamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer


class TeamRolesAPIView(APIView):
    def get(self, request):
        data = get_team_roles(request)
        response = Response(data)
        response['X-Header'] = 'Team roles info'
        return response


class ChangeMemberRoleAPIView(APIView):
    permission_classes = [IsAuthenticated, HasTeamRole]
    required_role = 'Admin'

    def post(self, request, pk, member_pk):
        new_role = request.data.get('selected_role')
        if not new_role:
            return Response({"error": "selected_role is required"}, status=400)

        result = change_member_role(request, pk, member_pk, new_role)
        return Response({
            "team_id": result['team'].pk,
            "member_id": result['member'].pk,
            "new_role": new_role
        }, status=status.HTTP_200_OK)



class TeamsDetailAPIView(generics.ListAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
