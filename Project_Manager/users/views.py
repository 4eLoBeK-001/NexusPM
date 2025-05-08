from django.shortcuts import render

from .forms import LoginUserForm, RegisterUserForm
# Create your views here.

def login_user(request):
    form = LoginUserForm()
    data = {
        'form': form
    }
    return render(request, 'users/login.html', data)

def register_user(request):
    form = RegisterUserForm()
    data = {
        'form': form
    }
    return render(request, 'users/register.html', data)