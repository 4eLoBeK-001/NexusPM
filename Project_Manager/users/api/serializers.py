from rest_framework import serializers

from teams.models import Team, TeamInvitation
from users.models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('id', 'phone_number')

    def get_phone_number(self, obj):
        if obj.hide_number:
            return 'Телефон скрыт'
        return obj.phone_number

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'profile', 'email',)
    
    def get_email(self, obj):
        if obj.profile.hide_email:
            return 'Почта скрыта'
        return obj.email


class TeamInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInvitation
        fields = ('team', 'invited_by', 'invited_user', 'created_at', 'accepted')