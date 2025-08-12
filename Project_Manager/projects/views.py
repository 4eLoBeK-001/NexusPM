from django.db.models import F, Q, Count    
from django.db.models import Subquery, OuterRef

from django.db.transaction import commit, atomic
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from users.models import ProjectMember, TeamMember

from teams.models import Team
from teams.utils.decorators import role_required

from projects.models import Project
from projects.forms import AddModalProjectForm, UpdateProjectForm

from tasks.models import Status, Tag
from tasks.forms import CreateStatusForm, CreateTagForm
from tasks.utils.decorators import require_project_member




def project_list(request, pk):
    team = get_object_or_404(Team, pk=pk)
    projects = Project.objects.for_team(team).filter(
        project_members=request.user
    ).select_related('team')
    form = AddModalProjectForm()
    context = {
        'team': team,
        'projects': projects,
        'status_choices': Project.StatusChoices,
        'form': form
    }
    return render(request, 'projects/project_list.html', context)


@login_required
def my_projects(request):
    projects = Project.objects.filter(project_members=request.user)
    context = {
        'projects': projects,
        'status_choices': Project.StatusChoices,
    }
    return render(request, 'projects/my_projects.html', context)


def search_projects(request, pk):
    team = get_object_or_404(Team, pk=pk)
    search = request.GET.get('search1', '')
    projects = Project.objects.for_team(team).filter(name__icontains=search, project_members=request.user)
    context = {
        'team': team,
        'status_choices': Project.StatusChoices,
        'projects': projects
    }
    return render(request, 'projects/projects.html', context)


@role_required('Admin')
@require_http_methods(['POST'])
def create_project(request, pk):
    form = AddModalProjectForm(request.POST, request.FILES)
    if form.is_valid():
        team_id = request.POST.get('team_id')
        team = get_object_or_404(Team, id=team_id)

        project = form.save(commit=False)
        project.team = team
        project.save()

        all_practicants = request.POST.get('all_practicants', '')
        if all_practicants:
            project.project_members.add(*team.team_member.all().values_list('id', flat=True))
        else:
            project.project_members.add(request.user.id)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(request.META.get('HTTP_REFERER', '/'))


@role_required('Admin')
@require_project_member
def delete_project(request, project_pk, *args, **kwargs):
    response = redirect(request.META.get('HTTP_REFERER'))
    project = get_object_or_404(Project, pk=project_pk)
    project.tags.all().delete()
    project.statuses.all().delete()
    if request.GET.get('trigger') == 'detail':
        response = redirect(reverse('teams:projects:project_list', args=[project.team.pk]))
    project.delete()
    return response


@role_required('Manager')
@require_project_member
def project_status_changes(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    status = request.POST.get('status')
    project.status = status
    project.save()
    data = {
        'project': project,
        'status_choices': Project.StatusChoices,
    }
    return render(request, 'projects/includes/change-status.html', data)


@require_project_member
def project_settings(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    form = UpdateProjectForm(instance=project)
    data = {
        'project': project,
        'form': form
    }
    return render(request, 'projects/includes/setting.html', data)


@role_required('Admin')
@require_http_methods(['POST'])
@require_project_member
def change_project(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    form = UpdateProjectForm(request.POST, request.FILES, instance=project)
    if form.is_valid():
        form.save()
    return redirect(request.META.get('HTTP_REFERER'))


# @require_project_member

def project_members(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    team = project.team
    roles = TeamMember.RoleChoices.choices
    
    # формируется подзапрос для подсчёта количества проектов в команде,
    # в которых участвует конкретный пользователь
    project_count_subquery = ProjectMember.objects.filter(
        user=OuterRef('pk'),
        project__team=team
    ).values('user').annotate(count=Count('project')).values('count')

    # Тут в queryset добавляется:
    # Количество проектов в командде, где участвует пользователь
    # Дату присоединения к проекту
    project_members = project.project_members.annotate(
        projects_count=Subquery(project_count_subquery),
        date_joining=F('members_projects__date_joining')
    ).select_related('profile')

    # Cписок всех участников команды
    team_members = team.team_member.select_related('profile')

    data = {
        'team': team,
        'project': project,
        'project_members': project_members,
        'project_member_ids': project_members.values_list('id', flat=True),
        'team_members': team_members,
        'roles': roles
    }
    return render(request, 'projects/includes/members.html', data)


@role_required('Admin')
@require_http_methods(['POST'])
@require_project_member
def delete_project_members(request, project_pk, member_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    member = get_object_or_404(get_user_model(), pk=member_pk)

    # Убирается пользователь из участников проекта
    project.project_members.remove(member_pk)
    
    # Переменная содержит все задачи в проекте, где этот пользователь является исполнителем
    tasks_where_user_is_executor = member.assigned_tasks.filter(project=project)

    # Удаляются все исполнители
    for task in tasks_where_user_is_executor:
        task.executor.remove(member_pk)

    return render(request, 'projects/includes/member.html')


@role_required('Admin')
@require_http_methods(['POST'])
@require_project_member
def add_project_members(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    members_ids = request.POST.getlist('member')
    project.project_members.set(members_ids)

    return redirect(request.META.get('HTTP_REFERER'))


@require_project_member
def search_members(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    text = request.GET.get('input_search')
    team = project.team

    # Формируется подзапрос для подсчёта количества проектов в команде,
    # в которых участвует конкретный пользователь
    project_count_subquery = ProjectMember.objects.filter(
        user=OuterRef('pk'),
        project__team=team
    ).values('user').annotate(count=Count('project')).values('count')

    # Фильтрация участников проекта по username и email
    project_members = project.project_members.annotate(
        projects_count=Subquery(project_count_subquery),
        date_joining=F('members_projects__date_joining')
    ).filter(Q(username__icontains=text) | Q(email__icontains=text))

    data = {
        'project': project,
        'project_members': project_members,
    }
    return render(request, 'projects/includes/member.html', data)


@require_project_member
def project_tags(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    tags = project.tags.select_related('color')
    form = CreateTagForm()
    data = {
        'project': project,
        'tags': tags,
        'create_tag_form': form
    }
    return render(request, 'projects/includes/tags.html', data)


@role_required('Member')
@require_http_methods(['POST'])
@require_project_member
def delete_tag(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    tags = project.tags.all()
    selected_tag = request.POST.get('tag_id')
    tag = get_object_or_404(Tag, pk=int(selected_tag))
    tag.delete()
    data = {
        'project': project,
        'tags': tags
    }
    return render(request, 'projects/includes/tag.html', data)


@require_project_member
def search_tags(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    req = request.GET.get('input_search')
    tags = project.tags.filter(Q(name__icontains=req) | Q(color__name__icontains=req))
    data = {
        'project': project,
        'tags': tags
    }
    return render(request, 'projects/includes/tags_list_partial.html', data)


@role_required('Member')
@require_http_methods(['POST'])
@require_project_member
def create_tag(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    form = CreateTagForm(request.POST)
    if form.is_valid():
        tag = form.save(commit=False)
        tag.project = project
        tag.save()
    return redirect(request.META.get('HTTP_REFERER'))


@require_project_member
def project_statuses(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    statuses = project.statuses.select_related('color')
    form = CreateStatusForm()
    data = {
        'project': project,
        'statuses': statuses,
        'form': form
    }
    return render(request, 'projects/includes/statuses.html', data)


@role_required('Manager')
@require_http_methods(['POST'])
@require_project_member
def create_status(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    form = CreateStatusForm(request.POST)
    if form.is_valid():
        status = form.save(commit=False)
        status.project = project
        status.save()
    return redirect(request.META.get('HTTP_REFERER'))


@require_project_member
def search_status(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    req = request.GET.get('input_search')
    statuses = Status.objects.filter(Q(name__icontains=req) | Q(color__name__icontains=req))
    data = {
        'project': project,
        'statuses': statuses,
    }
    return render(request, 'projects/includes/status-list.html', data)


@role_required('Manager')
@require_http_methods(['POST'])
@require_project_member
def delete_status(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    statuses = project.statuses.all()
    status_id = request.POST.get('status_id')
    status = get_object_or_404(Status, pk=status_id)
    status.delete()
    data = {
        'project': project,
        'statuses': statuses,
    }
    return render(request, 'projects/includes/status.html', data)

