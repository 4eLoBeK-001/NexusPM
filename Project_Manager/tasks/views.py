from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from projects.models import Project

from tasks.models import Status, Tag, Task
from tasks.forms import SidebarForm, UpdateTaskForm



def task_list(request, project_pk, team_pk):
    project = get_object_or_404(Project, pk=project_pk)
    tasks = Task.objects.filter(project=project)
    statuses = Status.objects.all()
    context = {
        'tasks': tasks,
        'statuses': statuses,
    }
    return render(request, 'tasks/task_list.html', context)

@require_http_methods(['POST'])
def change_status(request, task_pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=task_pk)
    statuses = Status.objects.all()
    
    status_id = int(request.POST.get('status_id'))
    status = get_object_or_404(Status, pk=status_id)
    task.status = status
    task.save()
    data = {
        'task': task, 
        'statuses': statuses
    }
    return render(request, 'tasks/includes/change-status.html', data)


def task_detail(request, task_pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=task_pk)
    project = task.project
    tags = Tag.objects.filter(project=project)
    form = UpdateTaskForm(instance=task, project=project)
    if request.method == 'POST':
        tag_list_ids = request.POST.getlist('tag')
        tags_list = Tag.objects.filter(id__in=tag_list_ids)
        task.tag.set(tags_list)
        return redirect(request.META.get('HTTP_REFERER'))
    data = {
        'task': task,
        'tags': tags,
        'form': form
    }
    return render(request, 'tasks/task-detail.html', data)


def test_tags(request, task_pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=task_pk)
    project = task.project
    tags = Tag.objects.filter(project=project)

    if request.method == 'POST':
        form = SidebarForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.project = project
            tag.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = SidebarForm()

    data = {
        'task': task,
        'tags': tags,
        'form': form
    }
    return render(request, 'tasks/test_place.html', data)