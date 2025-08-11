from django.contrib import admin

from .models import Project
from users.models import ProjectMember


@admin.display(description='Удалить всех участников')
def delete_all_members(modeladmin, request, queryset):
    if queryset.model == Project:
        for project in queryset:
            project.project_members.clear()


class ProjectMembers(admin.TabularInline):
    model = Project.project_members.through
    extra = 4
    max_num = 10


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description', 'team__name', 'created_at', 'updated_at')
    list_display_links = ('name', 'team__name')
    ordering = ('-created_at',)
    list_filter = ('team',)
    search_fields = ('name', 'team__name')

    actions = (delete_all_members,)

    fields = ('name', 'description', 'team', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    inlines = [
        ProjectMembers
    ]

    @admin.display(description='Description')
    def short_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project', 'user')
    readonly_fields = ('date_joining',)


ProjectMember._meta.app_label = 'projects'