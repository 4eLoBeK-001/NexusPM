from .models import Team

def all_teams_processor(request):
    return {
        'context_teams': Team.objects.all()
    }