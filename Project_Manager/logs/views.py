from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from tasks.models import Task
from projects.models import Project
from teams.models import Team
from logs.models import ActionLog


@login_required
def history(request):
    logs = ActionLog.objects.filter(participants=request.user
    ).select_related('team', 'project', 'task', 'user'
    ).distinct().order_by('-created_at')
    
    # Получаем уникальные команды/проекты/задачи из логов
    teams = Team.objects.filter(id__in=logs.values_list('team', flat=True)).distinct()
    projects = Project.objects.filter(id__in=logs.values_list('project', flat=True)).distinct()
    tasks = Task.objects.filter(id__in=logs.values_list('task', flat=True)).distinct()
    
    action_types = ActionLog.ACTION_CHOICES

    data = {
        'logs': logs,
        'teams': teams,
        'projects': projects,
        'tasks': tasks,
        'action_types': action_types
    }
    return render(request, 'logs/history.html', data)


def history_search(request):
    search = request.GET.get('search_actions', '')

    logs = ActionLog.objects.filter(participants=request.user)

    if search:
        logs = logs.filter(
            Q(team__name__icontains=search) |
            Q(project__name__icontains=search) |
            Q(task__name__icontains=search) 
        )

    data = {
        'logs': logs.distinct().order_by('-created_at'),
    }
    return render(request, 'logs/history_list.html', data)


def history_filter(request):
    filters = {
        'team__id': request.GET.get('team', ''),
        'project__id': request.GET.get('project', ''),
        'task__id': request.GET.get('task', ''),
        'action_type': request.GET.get('action_type', ''),
    }

    # Удаляются пустые значения из фильтров
    filters = {k: v for k, v in filters.items() if v}

    logs = ActionLog.objects.filter(
        participants=request.user,
        **filters
    ).distinct().order_by('-created_at')
    
    data = {
        'logs': logs,
    }
    return render(request, 'logs/history_list.html', data)


def team_history(request, pk):

    team = get_object_or_404(Team, pk=pk)
    projects = team.projects.all()
    tasks = Task.objects.filter(project_id__in=projects.values_list('id', flat=True))
    action_types = ActionLog.ACTION_CHOICES

    logs = ActionLog.objects.filter(
        participants=request.user, team=team
    ).select_related('team', 'project', 'task', 'user')

    context = {
        'team': team,
        'projects': projects,
        'tasks': tasks,
        'action_types': action_types,
        'logs': logs,
    }
    return render(request, 'logs/team_history.html', context)


def project_history(request, pk, project_pk):

    project = get_object_or_404(Project, pk=project_pk)
    tasks = project.tasks.all()
    action_types = ActionLog.ACTION_CHOICES
    
    logs = ActionLog.objects.filter(
        participants=request.user, project=project
    ).select_related('team', 'project', 'task', 'user')

    context = {
        'tasks': tasks,
        'project': project,
        'action_types': action_types,
        'logs': logs,
    }
    return render(request, 'logs/project_history.html', context)
