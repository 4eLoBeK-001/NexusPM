from django.shortcuts import get_object_or_404, render

from teams.models import Team

# Create your views here.

def main_page(request):
    return render(request, 'home-page.html')

def project_list(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'teams/project_list.html')

def project_lst(request):
    return render(request, 'teams/project_list_lst.html')

def project_card(request):
    return render(request, 'teams/project_list_t.html')