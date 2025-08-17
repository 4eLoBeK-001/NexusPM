from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from teams.api.permissions import HasTeamRole
from teams.api.filters import TeamFilter, TeamMemberFilter
from users.models import TeamMember, User
from teams.models import Team, TeamInvitation
from teams.api.serializers import SendInvitationSerializer, TeamListSerializer, TeamDetailSerializer, TeamMemberSerializer
from teams.services import get_team_roles, change_member_role


class TeamListCreateAPIView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamListSerializer
    permission_classes = [IsAuthenticated, HasTeamRole]
    required_role = 'Admin'
    filterset_class = TeamFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = ['created_at']
    filterset_fields = ['author']

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


class TeamMembersAPIView(generics.ListAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TeamMemberFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        'user__username': ['exact', 'icontains'],
    }
    ordering_fields = ['date_joining']

    def get_queryset(self):
        qs = super().get_queryset()
        team_pk = self.kwargs['pk']
        return qs.filter(team_id=team_pk)


    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response['X-Header'] = 'List of team members'

        team_pk = self.kwargs['pk']
        team = Team.objects.get(pk=team_pk)

        response.data = {
            'team': {'id': team.id, 'name': team.name},
            'members': response.data
        }
        return response


class TeamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasTeamRole]
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    required_role = 'Admin'


class LeaveFromTeamApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        membership = get_object_or_404(TeamMember, team=team, user=request.user)

        if membership.role == TeamMember.RoleChoices.CREATOR:
            return Response(
                {'detail': 'Создатель команды не может выйти. Передайте права другому пользователю'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        membership.delete()
        return Response({'detail': 'Вы успешно покинули команду'}, status=status.HTTP_204_NO_CONTENT)


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


class SendInvitationToTeamAPIView(APIView):
    serializer_class = SendInvitationSerializer

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        team = get_object_or_404(Team, pk=pk)
        if serializer.is_valid():
            emails = serializer.validated_data.get('emails')
            valid_emails = emails.get('valid_emails')
            invalid_emails = emails.get('invalid_emails')

            new_valid_emails = []

            for email in valid_emails:
                user = User.objects.filter(email=email).first()
                already_invited = TeamInvitation.objects.filter(team=team, invited_user=user, accepted=False).exists()
                
                if (not user) or (user in team.team_member.all()) or (already_invited):
                    invalid_emails.append(email)
                else:
                    new_valid_emails.append(email)
                    TeamInvitation.objects.create(team=team, invited_by=request.user, invited_user=user)
    
            return Response(
                {
                    'Отправлено приглашение': f'{len(new_valid_emails)} адресам',
                    'valid_emails': new_valid_emails, 
                    'Не удалось пригласить участников': f'{len(invalid_emails)} адресов',
                    'invalid_emails': invalid_emails,
                 }
                , status=200)
        return Response(serializer.errors, status=400)


class AcceptInvitationAPIView(generics.UpdateAPIView):
    queryset = TeamInvitation.objects.all()

    def update(self, request, pk, *args, **kwargs):
        try:
            team = get_object_or_404(Team, pk=pk)
            invitation = TeamInvitation.objects.get(team=team, invited_user=request.user, accepted=False)
            invitation.accepted=True
            invitation.save()
            team.team_member.add(request.user)
            return Response({'message':f'Приглашение принято. Вы успешно вступили в команду: {team.name}'})
        
        except ObjectDoesNotExist:
            return Response({'message': 'У вас нет приглашений в эту команду'}, status=status.HTTP_404_NOT_FOUND)