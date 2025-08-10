from django.contrib import admin

from .models import Project


class ProjectMember(admin.TabularInline):
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

    fields = ('name', 'description', 'team', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    inlines = [
        ProjectMember
    ]

    @admin.display(description='Description')
    def short_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description