from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.utils.html import format_html

from teams.utils.decorators import role_required

from projects.models import Project

from tasks.utils.decorators import require_project_member
from tasks.models import Comment, Status, Tag, Task, TaskImage
from tasks.forms import AddCommentForm, AddImageTaskForm, CreateStatusForm, CreateSubtaskForm, CreateTagForm, CreateTaskForm, UpdateTagForm, UpdateTaskForm



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


@role_required('Member')
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


@role_required('Member')
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
    project_members = task.project.project_members.all()
    executor_ids = task.executor.values_list('id', flat=True)
    create_subtask_form = CreateSubtaskForm()
    project = task.project
    executors = task.executor.all()
    statuses = Status.objects.all()
    tags = Tag.objects.filter(project=project)
    update_tag_form = UpdateTagForm(instance=task, project=project)
    create_tag_form = CreateTagForm()
    comment_form = AddCommentForm()
    task_form = UpdateTaskForm(instance=task)
    
    data = {
        'task': task,
        'project': project,
        'tags': tags,
        'statuses': statuses,
        'executors': executors,
        'update_tag_form': update_tag_form,
        'create_tag_form': create_tag_form,
        'task_form': task_form,
        'project_members': project_members,
        'executor_ids': executor_ids,
        'create_subtask_form': create_subtask_form,
        'comment_form': comment_form,
        'priorities': task.PriprityChoices
    }
    return render(request, 'tasks/task-detail.html', data)


@role_required('Member')
@require_http_methods(['POST'])
def change_task(request, task_pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=task_pk)
    task_form = UpdateTaskForm(request.POST, instance=task)
    if task_form.is_valid():
        task_form.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


@role_required('Member')
@require_http_methods(['POST'])
def processing_image(request, task_pk, *args, **kwargs):
    image = request.FILES.get('image_task')
    task = get_object_or_404(Task, pk=task_pk)
    TaskImage.objects.create(task=task, image=image)
    return redirect(request.META.get('HTTP_REFERER'))


@role_required('Member')
@require_http_methods(['POST'])
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


@role_required('Member')
@require_http_methods(['POST'])
def task_delete(request, task_pk, *args, **kwargs):
    task_pk = request.POST.get('task_pk') or request.POST.get('detail_task_pk')
    task = get_object_or_404(Task, pk=task_pk)
    task.delete()

    if 'detail_task_pk' in request.POST:
        return reverse('task_list', args=[task.project.team.pk, task.project.pk, task.pk])
    else:
        return redirect(request.META.get('HTTP_REFERER'))


@role_required('Member')
@require_http_methods(['POST'])
def change_tag(request, task_pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=task_pk)
    tag_list_ids = request.POST.getlist('tag')
    tags_list = Tag.objects.filter(id__in=tag_list_ids)
    task.tag.set(tags_list)
    return redirect(request.META.get('HTTP_REFERER'))


@role_required('Member')
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


@role_required('Member')
@require_http_methods(['POST'])
def add_executors(request, task_pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=task_pk)
    executors = request.POST.getlist('executor')
    task.executor.set(executors)
    return redirect(request.META.get('HTTP_REFERER'))


@role_required('Viewer')
@require_http_methods(['POST'])
def add_comment(request, task_pk, project_pk, **kwargs):
    comment_form = AddCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.task_id = task_pk
        comment.author = request.user
        comment.save()
    data = {
        'project': get_object_or_404(Project, pk=project_pk),
        'task': get_object_or_404(Task, pk=task_pk),
        'comment': comment
    }
    return render(request, 'tasks/includes/comment.html', data)


@role_required('Member')
@require_http_methods(['POST'])
def delete_comment(request, comm_pk, *args, **kwargs):
    comment = get_object_or_404(Comment, pk=comm_pk)
    comment.delete()
    return render(request, 'tasks/includes/comment.html')
