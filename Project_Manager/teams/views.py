from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils.html import format_html

from .forms import AddModalTeamForm, AddTeamForm
from .models import Team


def workplace(request):
    return render(request, 'teams/workplace.html')


def team_list(request):
    teams = Team.objects.all()
    team_forms = {team.id: AddModalTeamForm(instance=team) for team in teams}
    context = {
        'teams': teams,
        'team_forms': team_forms,
    }
    return render(request, 'teams/team_list.html', context)


def team_conf(request, pk):
    team = Team.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddTeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = AddTeamForm(instance=team)
    context = {
        'team': team,
        'form': form
    }
    return render(request, 'teams/includes/setting.html', context)

def team_members(request, pk):
    team = Team.objects.get(pk=pk)
    context = {
        'team': team,
    }
    return render(request, 'teams/includes/team_members.html', context)

@require_http_methods(['POST'])
def create_team(request):
    form = AddModalTeamForm(request.POST, request.FILES)
    if form.is_valid():
        team = form.save(commit=False)
        team.author = request.user
        team.save()
        messages.success(
            request, 
            message=format_html(
                'Команда  <a id="mtl" href="{}">{}</a>  успешно создана',
                reverse('teams:projects:project_list', args=[team.id]),
                team.name
            ),
        )
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


# @require_http_methods(['PUT', 'PATCH'])
def update_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = AddModalTeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))
    
    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))


@require_http_methods(['GET'])
def search_team(request):
    search = request.GET.get('search', '')
    queryset = Team.objects.filter(name__icontains=search)
    team_forms = {team.id: AddModalTeamForm(instance=team) for team in queryset}

    return render(request, 'teams/partial-team_list.html', {'teams': queryset, 'team_forms': team_forms})


@require_http_methods(['GET'])
def sidebar_search_team(request):
    search = request.GET.get('search', '')
    queryset = Team.objects.filter(name__icontains=search)
    return render(request, 'includes/team_list.html', {'context_teams': queryset})


def delete_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    team.delete()
    return redirect(request.META.get('HTTP_REFERER'))
    