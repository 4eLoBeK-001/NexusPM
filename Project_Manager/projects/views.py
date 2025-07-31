from django.db.models import F, Q, Count    
from django.db.models import Subquery, OuterRef

from django.db.transaction import commit
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model

from users.models import ProjectMember
from teams.models import Team

from projects.models import Project
from projects.forms import AddModalProjectForm, UpdateProjectForm

from tasks.models import Status, Tag
from tasks.forms import CreateStatusForm, CreateTagForm
from tasks.utils.decorators import require_project_member




def project_list(request, pk):
    team = get_object_or_404(Team, pk=pk)
    projects = Project.objects.filter(team=team, project_members=request.user)
    form = AddModalProjectForm()
    context = {
        'team': team,
        'projects': projects,
        'status_choices': Project.StatusChoices,
        'form': form
    }
    return render(request, 'projects/project_list.html', context)



def search_projects(request, pk):
    team = get_object_or_404(Team, pk=pk)
    search = request.GET.get('search1', '')
    projects = Project.objects.filter(team=team, name__icontains=search, project_members=request.user)
    context = {
        'projects': projects
    }
    return render(request, 'projects/s.html', context)



@require_http_methods(['POST'])
def create_project(request):
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



@require_project_member
def delete_project(request, project_pk):
    response = redirect(request.META.get('HTTP_REFERER'))
    project = get_object_or_404(Project, pk=project_pk)
    if request.GET.get('trigger') == 'detail':
        response = redirect(reverse('teams:projects:project_list', args=[project.team.pk]))
    project.delete()
    return response


@require_project_member
def project_status_changes(request, project_pk):
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

    project_count_subquery = ProjectMember.objects.filter(
        user=OuterRef('pk'),
        project__team=team
    ).values('user').annotate(count=Count('project')).values('count')

    project_membersa = project.project_members.annotate(
        projects_count=Subquery(project_count_subquery),
        date_joining=F('members_projects__date_joining')
    ).all()

    team_members = team.team_member.all()

    data = {
        'project': project,
        'project_members': project_membersa,
        'project_member_ids': project_membersa.values_list('id', flat=True),
        'team_members': team_members,
    }
    return render(request, 'projects/includes/members.html', data)


@require_http_methods(['POST'])
@require_project_member
def delete_project_members(request, project_pk, member_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    member = get_object_or_404(get_user_model(), pk=member_pk)
    project.project_members.remove(member_pk)
    tasks_where_user_is_executor = member.assigned_tasks.filter(project=project)
    for task in tasks_where_user_is_executor:
        task.executor.remove(member_pk)

    return render(request, 'projects/includes/member.html')


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
    project_count_subquery = ProjectMember.objects.filter(
        user=OuterRef('pk'),
        project__team=team
    ).values('user').annotate(count=Count('project')).values('count')

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
    tags = project.tags.all()
    form = CreateTagForm()
    data = {
        'project': project,
        'tags': tags,
        'create_tag_form': form
    }
    return render(request, 'projects/includes/tags.html', data)


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
    statuses = project.statuses.all()
    form = CreateStatusForm()
    data = {
        'project': project,
        'statuses': statuses,
        'form': form
    }
    return render(request, 'projects/includes/statuses.html', data)


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

