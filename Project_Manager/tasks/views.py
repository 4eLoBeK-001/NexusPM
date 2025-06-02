from django.shortcuts import get_object_or_404, render

from projects.models import Project
from tasks.models import Status, Task

# Create your views here.

def task_list(request, project_pk, team_pk):
    project = get_object_or_404(Project, pk=project_pk)
    tasks = Task.objects.filter(project=project)
    statuses = Status.objects.all()
    context = {
        'tasks': tasks,
        'statuses': statuses
    }
    return render(request, 'tasks/task_list.html', context)