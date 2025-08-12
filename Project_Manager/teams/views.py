from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Q, F, Count, Sum

from users.models import User

from .forms import AddModalTeamForm, AddTeamForm, AddTeamMemberModalForm
from .models import Team, TeamInvitation
from .utils.decorators import role_required
from .utils.utils import get_role_description, ROLE_PERMISSIONS, PERMISSION_LABELS
from users.models import TeamMember


def workplace(request):
    return render(request, 'teams/workplace.html')

@login_required
def team_list(request):
    teams = Team.objects.is_member(request.user).select_related('author')
    team_forms = {team.id: AddModalTeamForm(instance=team) for team in teams}
    context = {
        'teams': teams,
        'team_forms': team_forms,
    }
    return render(request, 'teams/team_list.html', context)


@login_required
def team_conf(request, pk):
    team = Team.objects.get(pk=pk, team_member=request.user)
    form = AddTeamForm(instance=team)
    context = {
        'team': team,
        'form': form
    }
    return render(request, 'teams/includes/setting.html', context)


@login_required
def access_rights(request, pk):
    team = get_object_or_404(Team, pk=pk, team_member=request.user)
    roles = [
        {
            'value': role.value, 
            'label': role.label, 
            'rights': ROLE_PERMISSIONS[role.value], 
            'description': get_role_description(role.value)
        } 
        for role in TeamMember.RoleChoices
    ]

    context = {
        'team': team,
        'roles': roles,
        'rights_labels': PERMISSION_LABELS
    }
    return render(request, 'teams/includes/access_rights.html', context)



@role_required('Admin')
@require_http_methods(['POST'])
@login_required
def change_team(request, pk):
    team = get_object_or_404(Team, pk=pk, team_member=request.user)
    form = AddTeamForm(request.POST, request.FILES, instance=team)
    if form.is_valid():
        form.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def team_members(request, pk):
    team = Team.objects.get(pk=pk, team_member=request.user)
    form = AddTeamMemberModalForm()
    roles = TeamMember.RoleChoices.choices
    team_members = team.team_member.annotate(
        projects_count=Count('project_membership', filter=Q(project_membership__team=team)),
        member_date_joining=F('members_teams__date_joining'),
    ).select_related('profile')
    context = {
        'team': team,
        'form': form,
        'roles': roles,
        'team_members': team_members
    }
    return render(request, 'teams/includes/team_members.html', context)


@role_required('Admin')
@require_http_methods(['POST'])
@login_required
def change_role_member(request, pk, member_pk, *args, **kwargs):
    team = get_object_or_404(Team, pk=pk, team_member=request.user)
    member = team.participate_in_team.select_related('user').get(user_id=member_pk)
    selected_role = request.POST.get('selected_role')
    member.role = selected_role
    roles = TeamMember.RoleChoices.choices
    member.save()
    team_member = team.team_member.annotate(
        projects_count=Count('project_membership', filter=Q(project_membership__team=team)),
        member_date_joining=F('members_teams__date_joining')
    ).get(pk=member.user.pk)
    context = {
        'team': team,
        'member': team_member,
        'roles': roles
    }
    return render(request, 'teams/includes/team_members_list.html', context)



@role_required('Admin')
@require_http_methods(['POST'])
@login_required
def send_invitation_to_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    form = AddTeamMemberModalForm(request.POST)
    if form.is_valid():
        emails = form.cleaned_data.get('email')
        not_fould_emails = []
        for email in emails:
            user = get_user_model().objects.filter(email=email).first()

            if user: 
                # проверка, что пользователь не уже участник и не приглашён
                already_invited = TeamInvitation.objects.filter(team=team, invited_user=user, accepted=False).exists()
                already_member = user.members_teams.filter(team=team).exists()
                if not already_member and not already_invited:
                    TeamInvitation.objects.create(team=team, invited_by=request.user, invited_user=user)
                else:
                    not_fould_emails.append(email)
            else:
                not_fould_emails.append(email)
        
        if not_fould_emails:
            form.add_error(
                'email',
                mark_safe(f'Пользователи с адресами <strong>{', '.join(not_fould_emails)}</strong> не найдены или уже находятся в команде')
            )
            return render(request, 'teams/includes/team_members.html', {'form': form, 'team': team})
    else:
        return render(request, 'teams/includes/team_members.html', {'form': form, 'team': team})
    return redirect(request.META.get('HTTP_REFERER'))


@role_required('Admin')
@require_http_methods(['POST'])
@login_required
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


@login_required
@require_http_methods(['POST'])
@login_required
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



@require_http_methods(['GET'])
@login_required
def search_team(request):
    search = request.GET.get('search', '')
    queryset = Team.objects.is_member(request.user).filter(name__icontains=search)
    team_forms = {team.id: AddModalTeamForm(instance=team) for team in queryset}

    return render(request, 'teams/partial-team_list.html', {'teams': queryset, 'team_forms': team_forms})


@require_http_methods(['GET'])
@login_required
def sidebar_search_team(request):
    search = request.GET.get('search', '')
    queryset = Team.objects.is_member(request.user).filter(name__icontains=search)
    return render(request, 'teams/includes/team_list.html', {'context_teams': queryset})


def get_team_and_redirect(request, pk):
    response = redirect(request.META.get('HTTP_REFERER'))
    team = get_object_or_404(Team, pk=pk, team_member=request.user)
    if request.GET.get('trigger') == 'detail':
        response = redirect('teams:team_list')
    return team, response


@role_required('Creator')
@require_http_methods(['POST'])
@login_required
def delete_team(request, pk):
    team, response = get_team_and_redirect(request, pk)
    team.delete()
    return response


@require_http_methods(['POST'])
@login_required
def leave_from_team(request, pk):
    team, response = get_team_and_redirect(request, pk)
    team.team_member.remove(request.user.pk)
    return response


@require_http_methods(['GET'])
@login_required
def search_team_members(request, pk):
    team = get_object_or_404(Team, pk=pk)
    search = request.GET.get('input_search')
    roles = TeamMember.RoleChoices.choices
    team_members = team.team_member.annotate(
        projects_count=Count('project_membership', filter=Q(project_membership__team=team)),
        member_date_joining=F('members_teams__date_joining'),
        member_pks=F('members_teams__user_id')
    ).filter(Q(username__icontains=search) | Q(email__icontains=search))
    context = {
        'team_members': team_members,
        'team': team,
        'roles': roles
    }
    return render(request, 'teams/includes/team_members_list.html', context)
