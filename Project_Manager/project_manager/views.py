from django.shortcuts import render

def main_page(request):
    return render(request, 'home-page.html')


def notifications(request):
    return render(request, 'notifications.html')