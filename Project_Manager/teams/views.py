from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import AddTeamForm
from .models import Team


def workplace(request):
    
    return render(request, 'teams/workplace.html')

def team_list(request):
    teams = Team.objects.all()
    context = {
        'teams': teams
    }
    return render(request, 'teams/team_list.html', context)

@require_http_methods(['POST'])
def create_team(request):
    form = AddTeamForm(request.POST)
    if form.is_valid():
        team = form.save(commit=False)
        team.author = request.user
        team.save()
    return redirect(request.META.get('HTTP_REFERER'))