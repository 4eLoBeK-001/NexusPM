from rest_framework import serializers

from teams.models import Team

class TeamListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'name', 'short_description', 'author', 'team_member', 'created_at')
        read_only_fields = ('author',)

    def get_short_description(self, obj):
        if obj.description:
            return ' '.join(obj.description.split()[:10])
        return ''


class TeamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ('author', 'color')