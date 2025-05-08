from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from .forms import LoginUserForm, RegisterUserForm
# Create your views here.

def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect(reverse('projects:home'))

    else:
        form = LoginUserForm(request)
    data = {
        'form': form
    }
    return render(request, 'users/login.html', data)

def logout_user(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.save(commit=False)
            user.set_password(cd['password1'])
            user.save()
            return redirect(reverse('projects:home'))
    else:
        form = RegisterUserForm()
    data = {
        'form': form
    }
    return render(request, 'users/register.html', data)