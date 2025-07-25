from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from users.models import User

from .forms import AddModalTeamForm, AddTeamForm, AddTeamMemberModalForm
from .models import Team


def workplace(request):
    return render(request, 'teams/workplace.html')


def team_list(request):
    teams = Team.objects.filter(team_member=request.user)
    team_forms = {team.id: AddModalTeamForm(instance=team) for team in teams}
    context = {
        'teams': teams,
        'team_forms': team_forms,
    }
    return render(request, 'teams/team_list.html', context)


def team_conf(request, pk):
    team = Team.objects.get(pk=pk, team_member=request.user)
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
    team = Team.objects.get(pk=pk, team_member=request.user)
    form = AddTeamMemberModalForm()
    context = {
        'team': team,
        'form': form
    }
    return render(request, 'teams/includes/team_members.html', context)

@require_http_methods(['POST'])
def add_team_member(request, pk):
    team = Team.objects.get(pk=pk, team_member=request.user)

    form = AddTeamMemberModalForm(request.POST)

    if form.is_valid():
        emails = form.cleaned_data['email']
        not_fould_emails = []

        for email in emails:
            user = get_user_model().objects.filter(email=email).first()
            if user:
                team.team_member.add(user.pk)
            else:
                not_fould_emails.append(email)
            
        if not_fould_emails:
            form.add_error(
                'email', 
                mark_safe(f'Пользователи с адресами: <strong>{', '.join(not_fould_emails)}</strong> не найдены')
            )
            return render(request, 'teams/includes/team_members.html', {'team': team, 'form': form})

    else:
        return render(request, 'teams/includes/team_members.html', {'team': team, 'form': form})
    return redirect(request.META.get('HTTP_REFERER'))


@require_http_methods(['POST'])
def deleting_team_members(request, pk, member_pk):
    # Удаляет сначала участника из всех проектов, а потом уже из команды
    team = get_object_or_404(Team, pk=pk, team_member=request.user)
    project_members_list = team.projects.filter(project_members__id=member_pk) # Все проекты в которых он присутствует
    member = get_object_or_404(get_user_model(), pk=member_pk)

    for project in project_members_list:
        tasks = member.assigned_tasks.filter(project=project)
        for task in tasks:
            task.executor.remove(member_pk)
        project.project_members.remove(member_pk)

    team.team_member.remove(member_pk)
    return render(request, 'teams/includes/team_members_list.html')


@require_http_methods(['POST'])
def create_team(request):
    form = AddModalTeamForm(request.POST, request.FILES)
    if form.is_valid():
        team = form.save(commit=False)
        team.author = request.user
        team.save()
        team.team_member.set([request.user.id])
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
    queryset = Team.objects.filter(team_member=request.user, name__icontains=search)
    team_forms = {team.id: AddModalTeamForm(instance=team) for team in queryset}

    return render(request, 'teams/partial-team_list.html', {'teams': queryset, 'team_forms': team_forms})


@require_http_methods(['GET'])
def sidebar_search_team(request):
    search = request.GET.get('search', '')
    queryset = Team.objects.filter(name__icontains=search)
    return render(request, 'includes/team_list.html', {'context_teams': queryset})


def delete_team(request, pk):
    response = redirect(request.META.get('HTTP_REFERER'))
    team = get_object_or_404(Team, pk=pk, team_member=request.user)
    if request.GET.get('trigger') == 'detail':
        response = redirect('teams:team_list')
    team.delete()
    return response
    