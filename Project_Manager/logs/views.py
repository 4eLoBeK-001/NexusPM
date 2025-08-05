from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from tasks.models import Task
from projects.models import Project
from teams.models import Team
from logs.models import ActionLog


@login_required
def history(request):
    logs = ActionLog.objects.filter(participants=request.user).distinct().order_by('-created_at')
    
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
    return render(request, 'history.html', data)


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
    return render(request, 'history_list.html', data)


def history_filter(request):
    team_id = request.GET.get('team', '')
    project_id = request.GET.get('project', '')
    task_id = request.GET.get('task', '')
    action_type = request.GET.get('action_type', '')

    logs = ActionLog.objects.filter(participants=request.user)
    
    if team_id:
        logs = logs.filter(team_id=team_id)
    if project_id:
        logs = logs.filter(project_id=project_id)
    if task_id:
        logs = logs.filter(task_id=task_id)
    if action_type:
        logs = logs.filter(action_type=action_type)
    
    logs = logs.distinct().order_by('-created_at')
    
    data = {
        'logs': logs,
    }
    return render(request, 'history_list.html', data)