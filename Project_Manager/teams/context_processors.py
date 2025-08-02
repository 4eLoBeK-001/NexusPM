from django.contrib.auth.decorators import login_required

from .models import Team
from users.models import TeamMember
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


def role_proccessor(request):
    team_pk = None
    if hasattr(request, 'resolver_match'):
        team_pk = request.resolver_match.kwargs.get('pk')

    if not request.user.is_authenticated or not team_pk:
        return {}

    member = TeamMember.objects.get(team_id=team_pk, user=request.user)
    print(member.role)
    return {
        'your_role': member.role
    }

