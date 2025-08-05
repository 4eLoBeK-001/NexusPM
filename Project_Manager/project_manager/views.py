from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from tasks.models import Task
from projects.models import Project
from teams.models import Team
from logs.models import ActionLog

def main_page(request):
    return render(request, 'home-page.html')

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


def history_filter(request):
    team_id = request.GET.get('team', '')
    project_id = request.GET.get('project', '')
    task_id = request.GET.get('task', '')
    action_type = request.GET.get('action_type', '')

    logs = ActionLog.objects.filter(participants=request.user).distinct().order_by('-created_at')
    action_types = ActionLog.ACTION_CHOICES
    
    teams = Team.objects.filter(id__in=logs.values_list('team', flat=True)).distinct()
    projects = Project.objects.filter(id__in=logs.values_list('project', flat=True)).distinct()
    tasks = Task.objects.filter(id__in=logs.values_list('task', flat=True)).distinct()
    
    if team_id:
        logs = logs.filter(team_id=team_id).distinct().order_by('-created_at')
    if project_id:
        logs = logs.filter(project_id=project_id).distinct().order_by('-created_at')
    if task_id:
        logs = logs.filter(task_id=task_id).distinct().order_by('-created_at')
    if action_type:
        logs = logs.filter(action_type=action_type).distinct().order_by('-created_at')
    
    data = {
        'logs': logs,
        'teams': teams,
        'projects': projects,
        'tasks': tasks,
        'action_types': action_types
    }
    return render(request, 'history_list.html', data)