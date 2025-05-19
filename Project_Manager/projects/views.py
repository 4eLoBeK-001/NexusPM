from django.shortcuts import get_object_or_404, render

from projects.models import Project
from teams.models import Team

# Create your views here.

def main_page(request):
    return render(request, 'home-page.html')

def project_list(request, pk):
    team = get_object_or_404(Team, pk=pk)
    projects = Project.objects.filter(team=team)
    context = {
        'projects': projects
    }
    return render(request, 'teams/project_list.html', context)

def project_list_t(request):
    return render(request, 'teams/temp/project_list.html')

def project_lst(request):
    return render(request, 'teams/temp/project_list_lst.html')

def project_card(request):
    return render(request, 'teams/temp/project_list_t.html')