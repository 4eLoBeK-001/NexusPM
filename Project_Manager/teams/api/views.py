from rest_framework.response import Response
from rest_framework.decorators import api_view

from teams.models import Team
from teams.api.serializers import TeamSerializer

@api_view(['GET'])
def get_teams(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)