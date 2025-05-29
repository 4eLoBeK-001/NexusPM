from django.shortcuts import render

# Create your views here.

def task_list(request, project_pk, team_pk):
    return render(request, 'tasks/task_list.html')