from django.contrib import admin

from django.contrib.auth import get_user_model

from .models import TeamMember, TaskExecutor, ProjectMember
# Register your models here.

@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display= ('username', 'is_active', 'is_staff', 'is_superuser')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('team', 'user')
    readonly_fields = ('date_joining',)


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project', 'user')
    readonly_fields = ('date_joining',)


@admin.register(TaskExecutor)
class TaskExecutorAdmin(admin.ModelAdmin):
    list_display = ('task', 'user')