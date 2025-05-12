from .models import Team
from .forms import AddTeamForm

def all_teams_processor(request):
    return {
        'context_teams': Team.objects.all()
    }


def project_form_processor(request):
    return {'context_form': AddTeamForm()}