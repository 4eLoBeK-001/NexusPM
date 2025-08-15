from rest_framework import serializers

from teams.models import Team
from users.api.serializers import UserSerializer
from users.models import User, TeamMember

class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TeamMember
        fields = ('user', 'role', 'date_joining')


class TeamListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()
    memberships = TeamMemberSerializer(source='participate_in_team', many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'short_description', 'author', 'memberships', 'created_at')
        read_only_fields = ('author',)

    def get_short_description(self, obj):
        if obj.description:
            return ' '.join(obj.description.split()[:10])
        return ''


class TeamDetailSerializer(serializers.ModelSerializer):
    memberships = TeamMemberSerializer(source='participate_in_team', many=True, read_only=True)
    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'author', 'memberships', 'image', 'color', 'updated_at', 'created_at')
        read_only_fields = ('author', 'color',)