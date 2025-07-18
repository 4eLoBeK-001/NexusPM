from django.shortcuts import get_object_or_404
from django.http import Http404
from projects.models import Project
from functools import wraps

def require_project_member(view_func):
    @wraps(view_func)
    def wrapper(request, project_pk=None, *args, **kwargs):
        if project_pk is None:
            raise Http404("project_pk обязателен")
        
        project = get_object_or_404(Project, pk=project_pk)
        if request.user not in project.project_members.all():
            raise Http404("Нет доступа к этому проекту")
        
        request.project = project
        return view_func(request, project_pk=project_pk, *args, **kwargs)
    return wrapper

