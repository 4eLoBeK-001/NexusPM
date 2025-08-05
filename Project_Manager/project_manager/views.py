from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Count

from logs.models import ActionLog

def main_page(request):
    return render(request, 'home-page.html')

@login_required
def history(request):
    logs = ActionLog.objects.filter(Q(team__team_member=request.user) | Q(participants=request.user)).distinct().order_by('-created_at')
    print(logs)
    all_logs = []
    for log in logs:
        print(f'team - {log.team} | '
        f'project - {log.project if log.project else None} | '
        f'action - {log.action_type}')
        ...
    
    data = {
        'logs': logs
    }
    return render(request, 'history.html', data)