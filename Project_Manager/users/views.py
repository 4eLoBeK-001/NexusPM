from django.shortcuts import render

# Create your views here.

def login_user(request):
    return render(request, 'users/login.html')

def register_user(request):
    return render(request, 'users/register.html')