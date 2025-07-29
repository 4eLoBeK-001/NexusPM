from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.urls import reverse
from django.utils.html import format_html

from teams.models import TeamInvitation

from .models import Notifications, SocialNetwork, Tag

from .forms import AddSocialnetworkForm, AddTagForm, ChangeProfileForm, ChangeUserForm, LoginUserForm, RegisterUserForm
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
    tags = profile.tags.all()
    tag_form = AddTagForm()
    social_form = AddSocialnetworkForm()
    networks = [network[0] for network in SocialNetwork.SOCIAL_CHOICES]
    social_links = profile.social_links.all()
    data = {
        'user': user,
        'profile': profile,
        'social_links': social_links,
        'social_form': social_form,
        'networks': networks,
        'tag_form': tag_form,
        'tags': tags
    }
    return render(request, 'users/profile.html', data)


SOCIAL_LINKS  = {
    'Telegram': lambda username: 'https://t.me/' + username,
    'VK': lambda username: 'https://m.vk.com/id/' + username,
    'GitHub': lambda username: 'https://github.com/' + username,
}

@require_http_methods(['POST'])
def add_social_network(request):
    user = request.user    
    profile = user.profile
    social_form = AddSocialnetworkForm(request.POST, profile=profile)
    if social_form.is_valid():

        network = social_form.cleaned_data['network']
        username = social_form.cleaned_data['username']
        link = SOCIAL_LINKS[network](username)

        SocialNetwork.objects.create(
            profile=profile,
            network=network,
            link=link
        )
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        for error in social_form.non_field_errors():
            messages.error(request, error)

    return redirect(request.META.get('HTTP_REFERER'))


def delete_social_network(request, network_pk):
    network = get_object_or_404(SocialNetwork, pk=network_pk)
    network.delete()
    return redirect(request.META.get('HTTP_REFERER'))
    


def delete_user_tag(request, tag_pk):
    tag = get_object_or_404(Tag, pk=tag_pk)
    tag.delete()
    return redirect(request.META.get('HTTP_REFERER'))


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
        if 'profile_form' in request.POST or request.FILES.__len__()>0:
            profile_form = ChangeProfileForm(request.POST, request.FILES, instance=profile)
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


def notifications(request):
    notifications = Notifications.objects.filter(user=request.user)
    context = {
        'notifications': notifications
    }
    return render(request, 'notifications.html', context)


def notification_list(request):
    notifications = Notifications.objects.filter(user=request.user)
    context = {
        'notifications': notifications
    }
    return render(request, 'users/includes/notifications_list.html', context)


def invitation_list(request):
    invitations = TeamInvitation.objects.filter(invited_user=request.user)
    context = {
        'invitations': invitations
    }
    return render(request, 'users/includes/invitation_list.html', context)


def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(TeamInvitation, pk=invitation_id, invited_user=request.user)
    if not invitation.accepted:
        invitation.team.team_member.add(request.user)
        invitation.accepted = True
        invitation.save()
        messages.success(
            request,
            format_html(
                'Вы вступили в команду <a id="mtl" href={url}>{team}</a>',
                url=reverse('teams:projects:project_list', args=[invitation.team.id]),
                team=invitation.team.name
            )
        )
    return redirect(request.META.get('HTTP_REFERER'))
