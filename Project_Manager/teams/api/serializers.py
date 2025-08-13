from rest_framework import serializers

from teams.models import Team

class TeamSerializer(serializers.ModelSerializer):

    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('name', 'short_description', 'author', 'team_member', 'created_at')

    def get_short_description(self, obj):
        return ' '.join(obj.description.split()[:10]) # Первые 10 слов
    
