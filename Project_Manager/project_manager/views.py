from django.shortcuts import render
from logs.models import ActionLog

def main_page(request):
    return render(request, 'home-page.html')

def history(request):
    logs = ActionLog.objects.all()
    data = {
        'logs': logs
    }
    return render(request, 'history.html', data)