from django.db.models import Q
from django.db.transaction import commit
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from tasks.models import Tag
from projects.forms import AddModalProjectForm, UpdateProjectForm
from projects.models import Project
from teams.models import Team

# Create your views here.



def project_list(request, pk):
    team = get_object_or_404(Team, pk=pk)
    projects = Project.objects.filter(team=team)
    form = AddModalProjectForm()
    context = {
        'team': team,
        'projects': projects,
        'status_choices': Project.StatusChoices,
        'form': form
    }
    return render(request, 'projects/project_list.html', context)


def search_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    search = request.GET.get('search1', '')
    projects = Project.objects.filter(team=team, name__icontains=search)
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
            ...
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(request.META.get('HTTP_REFERER', '/'))


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def project_status_changes(request, pk):
    project = get_object_or_404(Project, pk=pk)
    status = request.POST.get('status')
    project.status = status
    project.save()
    data = {
        'project': project,
        'status_choices': Project.StatusChoices,
    }
    return render(request, 'projects/includes/change-status.html', data)


def project_settings(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    form = UpdateProjectForm(instance=project)
    if request.method == 'POST':
        form = UpdateProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    data = {
        'project': project,
        'form': form
    }
    return render(request, 'projects/includes/setting.html', data)


def project_members(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    data = {
        'project': project,
    }
    return render(request, 'projects/includes/members.html', data)


def project_tags(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    tags = project.tags.all()
    data = {
        'project': project,
        'tags': tags
    }
    return render(request, 'projects/includes/tags.html', data)


def delete_tag(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    tags = project.tags.all()
    if request.method == 'POST':
        selected_tag = request.POST.get('tag_id')
        tag = get_object_or_404(Tag, pk=int(selected_tag))
        tag.delete()
    data = {
        'project': project,
        'tags': tags
    }
    return render(request, 'projects/includes/tag.html', data)

def search_tags(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    req = request.GET.get('input_search')
    tags = project.tags.filter(Q(name__icontains=req) | Q(color__name__icontains=req))
    data = {
        'project': project,
        'tags': tags
    }
    return render(request, 'projects/includes/tags_list_partial.html', data)


def project_list_t(request):
    return render(request, 'projects/temp/project_list.html')

def project_lst(request):
    return render(request, 'projects/temp/project_list_lst.html')

def project_card(request):
    return render(request, 'projects/temp/project_list_t.html')