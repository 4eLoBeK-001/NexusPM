from django.shortcuts import get_object_or_404, render

from projects.models import Project
from tasks.models import Task

# Create your views here.

def task_list(request, project_pk, team_pk):
    project = get_object_or_404(Project, pk=project_pk)
    tasks = Task.objects.filter(project=project)
    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/task_list.html', context)