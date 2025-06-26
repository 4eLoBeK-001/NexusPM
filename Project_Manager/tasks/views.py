from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils.html import format_html

from projects.models import Project

from tasks.models import Status, Tag, Task
from tasks.forms import ChangeExecutorForm, CreateStatusForm, CreateSubtaskForm, CreateTagForm, CreateTaskForm, UpdateTagForm, UpdateTaskForm



def task_list(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    tasks = Task.objects.filter(project=project, parent_task__isnull=True)
    statuses = project.statuses.all()
    tags = project.tags.all()
    priorities = Task.PriprityChoices
    status_form = CreateStatusForm()
    task_form = CreateTaskForm()
    context = {
        'project': project,
        'tasks': tasks,
        'statuses': statuses,
        'tags': tags,
        'priorities': priorities,
        'form': status_form,
        'task_form': task_form
    }
    return render(request, 'tasks/task_list.html', context)


@require_http_methods(['POST'])
def create_task(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    task_form = CreateTaskForm(request.POST)
    if task_form.is_valid():
        task = task_form.save(commit=False)
        task.project = project
        task.creator = request.user
        task.save()
        messages.success(
            request,
            format_html('Задача <a id="mtl" href="{}">{}</a> успешно создана',
                reverse('teams:projects:tasks:task_detail', args=[project.team.pk, project.pk, task.pk]),
                task.name
            )
        )
    return redirect(request.META.get('HTTP_REFERER'))


def task_search(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)

    text = request.GET.get('input_search')
    tasks = Task.objects.filter(project=project, parent_task__isnull=True, name__icontains=text)

    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/includes/tasks.html', context)

def task_filter(request, project_pk, *args, **kwargs):
    project = get_object_or_404(Project, pk=project_pk)
    tasks = Task.objects.filter(project=project, parent_task__isnull=True)

    tag = request.GET.get('tag')
    if tag:
        tag_id = request.GET.get('tag')
        tasks = tasks.filter(tag__pk=tag_id)

    status = request.GET.get('status')
    if status:
        status_id = request.GET.get('status')
        tasks = tasks.filter(status__pk=status_id)

    priority = request.GET.get('priority')
    if priority:
        priority = request.GET.get('priority')
        tasks = tasks.filter(priority=priority)

    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/includes/tasks.html', context)


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
    create_subtask_form = CreateSubtaskForm()
    project = task.project
    executors = task.executor.all()
    statuses = Status.objects.all()
    tags = Tag.objects.filter(project=project)
    update_tag_form = UpdateTagForm(instance=task, project=project)
    create_tag_form = CreateTagForm()
    task_form = UpdateTaskForm(instance=task)
    
    if request.method == 'POST':
        
        if 'update_task' in request.POST:
            task_form = UpdateTaskForm(request.POST, instance=task)
            if task_form.is_valid():
                task_form.save()
                return redirect(request.META.get('HTTP_REFERER'))

        if 'update_tags' in request.POST:
            tag_list_ids = request.POST.getlist('tag')
            tags_list = Tag.objects.filter(id__in=tag_list_ids)
            task.tag.set(tags_list)
            return redirect(request.META.get('HTTP_REFERER'))

    data = {
        'task': task,
        'project': project,
        'tags': tags,
        'statuses': statuses,
        'executors': executors,
        'update_tag_form': update_tag_form,
        'create_tag_form': create_tag_form,
        'task_form': task_form,
        'create_subtask_form': create_subtask_form,
        'priorities': task.PriprityChoices
    }
    return render(request, 'tasks/task-detail.html', data)


def create_subtask(request, task_pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=task_pk)
    project = task.project
    form = CreateSubtaskForm(request.POST)
    if form.is_valid():
        subtask = form.save(commit=False)
        subtask.creator = request.user
        subtask.project = project
        subtask.parent_task = task
        subtask.save()
    return redirect(request.META.get('HTTP_REFERER'))


@require_http_methods(['POST'])
def task_delete(request, task_pk, *args, **kwargs):
    task_pk = request.POST.get('task_pk') or request.POST.get('detail_task_pk')
    task = get_object_or_404(Task, pk=task_pk)
    task.delete()

    if 'detail_task_pk' in request.POST:
        return reverse('task_list', args=[task.project.team.pk, task.project.pk, task.pk])
    else:
        return redirect(request.META.get('HTTP_REFERER'))


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


def test(request, task_pk, *args, **kwargs):
    data = {
    }
    return render(request, 'tasks/test_place.html', data)