from django.shortcuts import render

# Create your views here.

def workplace(request):
    return render(request, 'teams/workplace.html')