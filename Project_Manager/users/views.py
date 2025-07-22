from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from .forms import AddTagForm, ChangeProfileForm, ChangeUserForm, LoginUserForm, RegisterUserForm
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
    tag_form = AddTagForm()
    social_links = profile.social_links.all()
    data = {
        'user': user,
        'profile': profile,
        'social_links': social_links,
        'tag_form': tag_form
    }
    return render(request, 'users/profile.html', data)


@require_http_methods(['POST'])
def create_user_tag(request):
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
    profile = user.profile
    form = AddTagForm(request.POST)
    if form.is_valid():
        tag = form.save(commit=False)
        tag.profile = profile
        tag.save()
    return redirect(request.META.get('HTTP_REFERER'))


def change_profile(request):
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
    profile = user.profile
    user_form = ChangeUserForm(instance=user)
    profile_form = ChangeProfileForm(instance=profile)

    if request.method == 'POST':
        if 'user_form' in request.POST:
            user_form = ChangeUserForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                return redirect(request.META.get('HTTP_REFERER'))
        if 'profile_form' in request.POST:
            profile_form = ChangeProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect(request.META.get('HTTP_REFERER'))

    data = {
        'user': user,
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/change-profile.html', data)