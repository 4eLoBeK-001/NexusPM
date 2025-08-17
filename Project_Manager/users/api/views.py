from django.shortcuts import get_object_or_404
from django.template.context_processors import request

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from teams.models import Team, TeamInvitation
from users.api.serializers import TeamInvitationSerializer, UserSerializer
from users.models import User


class UsersListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class InvitationListApiView(generics.ListAPIView):
    queryset = TeamInvitation.objects.all()
    serializer_class = TeamInvitationSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(invited_user=self.request.user)