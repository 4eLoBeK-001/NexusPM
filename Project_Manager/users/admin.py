from django.contrib import admin, messages
from django.contrib.auth import get_user_model

from .models import TaskExecutor, ProjectMember, Profile, Tag, SocialNetwork, Feedback
# Register your models here.


def make_users(modeladmin, request, queryset, status):
    if queryset.model == get_user_model():
            updated_count = queryset.update(is_active=status)
            action = "разблокированы" if status else "заблокированы"
            messages.success(request, f"{updated_count} пользователь(ей) {action}.")

@admin.display(description='Заблокировать пользователей')
def block_users(modeladmin, request, queryset):
    make_users(modeladmin, request, queryset, False)

@admin.display(description='Разблокировать пользователей')
def unblock_users(modeladmin, request, queryset):
    make_users(modeladmin, request, queryset, True)


def make_staff_status(modeladmin, request, queryset, status):
    if queryset.model == get_user_model():
        updated_count = queryset.update(is_staff=status)
        action = 'выдан статус персонала' if status else 'втобран статус персонала'
        messages.success(request, f'{updated_count} пользователь(ям) {action}')

@admin.display(description='Забрать статус персонала')
def took_staff_status(modeladmin, request, queryset):
    make_staff_status(modeladmin, request, queryset, False)

@admin.display(description='Выдать статус персонала')
def give_staff_status(modeladmin, request, queryset):
    make_staff_status(modeladmin, request, queryset, True)



@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('username', 'email',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

    actions = (block_users, unblock_users, took_staff_status, give_staff_status)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'user__email', 'phone_number', 'short_description')
    list_display_links = ('user__username', 'user__email',)
    list_filter = ('phone_number', 'short_description')
    search_fields = ('user__username', 'short_description')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('profile__user__username', 'name', 'color')
    list_filter = ('name', 'color')
    search_fields = ('profile__user__username', 'name', 'color')
    

@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ('profile__user__username', 'network', 'link')
    list_filter = ('network',)
    search_fields = ('profile__user__username', 'network', 'link')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'content', 'user__username', 'is_answered', 'created_at')
    list_display_links = ('username', 'email', 'user__username',)
    list_filter = ('email', 'is_answered', 'created_at')
    search_fields = ('username', 'user__username', 'email')

    fields = ('username', 'email', 'content', 'user', 'is_answered', 'created_at', 'updated_at')
    readonly_fields = ('created_at',)

