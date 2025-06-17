from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from projects.models import Project

from tasks.models import Status, Tag, Task
from tasks.forms import CreateStatusForm, CreateTagForm, UpdateTaskForm



def task_list(request, project_pk, team_pk):
    project = get_object_or_404(Project, pk=project_pk)
    tasks = Task.objects.filter(project=project)
    statuses = Status.objects.filter(project=project)
    tags = project.tags.all()
    form = CreateStatusForm()

    context = {
        'project': project,
        'tasks': tasks,
        'statuses': statuses,
        'tags': tags,
        'form': form
    }
    return render(request, 'tasks/task_list.html', context)


def task_search(request, project_pk, team_pk):
    project = get_object_or_404(Project, pk=project_pk)

    text = request.GET.get('input_search')
    tasks = Task.objects.filter(project=project, name__icontains=text)

    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/includes/task.html', context)

def task_filter(request, project_pk, team_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'GET':
        ...

    tasks = Task.objects.filter(project=project)
    text = request.GET.get('tags')
    tag = get_object_or_404(Tag, pk=int(text))
    tasks = tasks.filter(tag=tag)

    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/includes/task.html', context)


@require_http_methods(['POST'])
def create_status(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    form = CreateStatusForm(request.POST)
    if form.is_valid():
        status = form.save(commit=False)
        status.project = project
        status.save()
    return redirect(request.META.get('HTTP_REFERER'))


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
    tag_form = CreateTagForm()
    if request.method == 'POST':

        tag_list_ids = request.POST.getlist('tag')
        tags_list = Tag.objects.filter(id__in=tag_list_ids)
        task.tag.set(tags_list)
        return redirect(request.META.get('HTTP_REFERER'))


    data = {
        'task': task,
        'project': project,
        'tags': tags,
        'form': form,
        'tag_form': tag_form,
        'priorities': task.PriprityChoices
    }
    return render(request, 'tasks/task-detail.html', data)


@require_http_methods(['POST'])
def change_priority(request, task_pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=task_pk)
    selected_priority = request.POST.get('priority', 'Не указан')
    task.priority = selected_priority
    task.save()
    data = {
        'task': task,
        'priorities': task.PriprityChoices
    }
    return render(request, 'tasks/includes/change-priority.html', data)
