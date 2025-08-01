from django.contrib.auth.decorators import login_required

from .models import Team
from .forms import AddModalTeamForm


def all_teams_processor(request):
    if request.user.is_authenticated:
        return {
            'context_teams': Team.objects.filter(team_member=request.user)
        }
    return {
        'comtext_teams': Team.objects.none()
    }


def project_form_processor(request):
    return {'context_form': AddModalTeamForm()}