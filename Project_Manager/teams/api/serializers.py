from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

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


class SendInvitationSerializer(serializers.Serializer):
    emails = serializers.CharField()

    def validate_emails(self, value):
        emails = [email.strip() for email in value.split(',')]
        valid_emails = []
        invalid_emails = []

        if not emails:
            raise serializers.ValidationError('Введите хотя-бы один email адрес')

        for email in emails:
            try:
                validate_email(email)
                valid_emails.append(email)
            except ValidationError:
                invalid_emails.append(email)

        return {
            'valid_emails': valid_emails,
            'invalid_emails': invalid_emails,
        }