from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout, get_user_model
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
                return redirect(reverse('home'))

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


def profile_user(request):
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
    profile = user.profile
    social_links = profile.social_links.all()
    data = {
        'user': user,
        'profile': profile,
        'social_links': social_links
    }
    return render(request, 'users/profile.html', data)