from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from logs.models import ActionLog

def main_page(request):
    return render(request, 'home-page.html')

@login_required
def history(request):
    logs = ActionLog.objects.all()
    data = {
        'logs': logs
    }
    return render(request, 'history.html', data)