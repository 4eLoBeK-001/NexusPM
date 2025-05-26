from django.contrib import admin

from .models import Project
# Register your models here.


class ProjectMember(admin.TabularInline):
    model = Project.project_members.through
    extra = 4


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'team', 'created_at', 'updated_at')
    list_display_links = ('name', 'team')

    readonly_fields = ('project_members',)

    inlines = [
        ProjectMember
    ]