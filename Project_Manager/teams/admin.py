from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import Team, TeamMember, TeamInvitation

class ProjectsCountFilter(admin.SimpleListFilter):
    title = 'Кол-во проектов / участников'
    parameter_name = 'count_filter'

    def lookups(self, request, model_admin):
        return (
            ('p_0', 'Нет проектов'),
            ('p_1>', 'Есть хотя бы один проект'),
            ('p_5>', 'Проекты: ≥ 5'),
            ('p_15>', 'Проекты: ≥ 15'),
            ('p_30>', 'Проекты: ≥ 30'),
            ('m_0', 'Нет участников (кроме автора)'),
            ('m_1>', 'Есть хотя бы один участник'),
            ('m_5>', 'Участники: ≥ 5'),
            ('m_15>', 'Участники: ≥ 15'),
            ('m_30>', 'Участники: ≥ 30'),
        )
    
    def queryset(self, request, queryset):

        value = self.value()
        if not value:
            return queryset

        kind, threshold = value.split('_')
        threshold_int = int(threshold.replace('>', ''))

        queryset = queryset.annotate(projects_count=Count('projects'), team_members=Count('team_member'))

        if kind == 'p':
            if '>' in threshold:
                return queryset.filter(projects_count__gte=threshold_int)
            return queryset.filter(projects_count=0)
        
        if kind == 'm':
            if '>' in threshold:
                return queryset.filter(team_members__gte=threshold_int)
            return queryset.filter(team_members=1)


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    max_num = 10


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'projects_and_members', 'get_short_description', 'author', 'created_at')
    list_display_links = ('name', 'author')
    ordering = ('-created_at',)
    list_filter = (ProjectsCountFilter,)
    search_fields = ('name', 'author__username')

    fields = ('name', 'description', 'author', 'image', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_projects_count=Count('projects'), _team_members=Count('team_member'))
    
    @admin.display(description="Проекты | Участники", ordering="_projects_count")
    def projects_and_members(self, obj):
        return format_html(
            '<span style="color:green;">{}</span> | <span style="color:blue;">{}</span>',
            obj._projects_count,
            obj._team_members
        )
    
    @admin.display(description='Description')
    def get_short_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description

    inlines = [
        TeamMemberInline
    ]


@admin.register(TeamInvitation)
class TeamInvitationAdmin(admin.ModelAdmin):
    list_display = ('team__name', 'invited_by', 'invited_user', 'accepted', 'created_at')
    list_display_links = ('team__name', 'invited_by', 'invited_user')
    ordering = ('-created_at',)
    list_filter = ('accepted',)
    search_fields = ('team', 'invited_by', 'invited_user')
    
    fields = ('team', 'invited_by', 'invited_user', 'accepted',  'created_at')
    readonly_fields = ('created_at',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('team__name', 'user', 'date_joining')
    list_display_links = ('team__name', 'user')
    ordering = ('-date_joining',)
    list_filter = ('team__name', 'user__username',)
    search_fields = ('team__name', 'user__username')

    fields = ('team', 'user', 'date_joining')
    readonly_fields = ('date_joining',)


TeamMember._meta.app_label = 'teams'
