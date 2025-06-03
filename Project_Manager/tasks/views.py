from django.shortcuts import get_object_or_404, render, redirect

from projects.models import Project

from tasks.models import Status, Task



def task_list(request, project_pk, team_pk):
    project = get_object_or_404(Project, pk=project_pk)
    tasks = Task.objects.filter(project=project)
    statuses = Status.objects.all()
    context = {
        'tasks': tasks,
        'statuses': statuses,
    }
    return render(request, 'tasks/task_list.html', context)


def change_status(request, team_pk, project_pk, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if request.method == 'POST':
        status_id = int(request.POST.get('selected_status'))
        status = get_object_or_404(Status, pk=status_id)
        task.status = status
        task.save()
        return redirect(request.META.get('HTTP_REFERER'))

