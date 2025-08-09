from django.contrib import admin

from .models import Team, TeamMember, TeamInvitation


class OrderItemInline(admin.TabularInline):
    model = TeamMember
    extra = 4
    max_num = 10


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_short_description', 'author', 'created_at')
    ordering = ('-created_at',)
    list_filter = ('author__username',)
    search_fields = ('name', 'author__username')

    fields = ('name', 'description', 'author', 'image', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Description')
    def get_short_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description

    inlines = [
        OrderItemInline
    ]


@admin.register(TeamInvitation)
class TeamInvitationAdmin(admin.ModelAdmin):
    list_display = ('team__name', 'invited_by', 'invited_user', 'accepted', 'created_at')
    ordering = ('-created_at',)
    list_filter = ('accepted',)
    search_fields = ('team', 'invited_by', 'invited_user')
    
    fields = ('team', 'invited_by', 'invited_user', 'accepted',  'created_at')
    readonly_fields = ('created_at',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('team__name', 'user', 'date_joining')
    ordering = ('-date_joining',)
    list_filter = ('team__name', 'user__username',)
    search_fields = ('team__name', 'user__username')

    fields = ('team', 'user', 'date_joining')
    readonly_fields = ('date_joining',)


TeamMember._meta.app_label = 'teams'
