from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from projects.forms import AddModalProjectForm
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
        project.project_members.add(*team.team_member.all().values_list('id', flat=True))
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

def project_list_t(request):
    return render(request, 'projects/temp/project_list.html')

def project_lst(request):
    return render(request, 'projects/temp/project_list_lst.html')

def project_card(request):
    return render(request, 'projects/temp/project_list_t.html')