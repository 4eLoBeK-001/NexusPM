from .models import Team
from .forms import AddModalTeamForm

def all_teams_processor(request):
    return {
        'context_teams': Team.objects.filter(team_member=request.user)
    }


def project_form_processor(request):
    return {'context_form': AddModalTeamForm()}