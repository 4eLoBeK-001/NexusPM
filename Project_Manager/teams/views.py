from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .forms import AddTeamForm
from .models import Team


def workplace(request):
    
    return render(request, 'teams/workplace.html')

def team_list(request):
    teams = Team.objects.all()
    team_forms = {team.id: AddTeamForm(instance=team) for team in teams}
    context = {
        'teams': teams,
        'team_forms': team_forms,
    }
    return render(request, 'teams/team_list.html', context)



@require_http_methods(['POST'])
def create_team(request):
    form = AddTeamForm(request.POST)
    if form.is_valid():
        team = form.save(commit=False)
        team.author = request.user
        team.save()
        messages.success(
            request, 
            message=f'Команда {team.name} успешно создана',
            extra_tags=team.id
        )
    return redirect(request.META.get('HTTP_REFERER'))

# @require_http_methods(['PUT', 'PATCH'])
def update_team(request, pk):
    team = Team.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddTeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


@require_http_methods(['GET'])
def search_team(request):
    search = request.GET.get('search', '')
    queryset = Team.objects.filter(name__icontains=search)
    return render(request, 'includes/team_list.html', {'context_teams': queryset})