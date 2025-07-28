from django.contrib import admin

from .models import Team
from .models import TeamMember, TeamInvitation


admin.site.register(TeamInvitation)

class OrderItemInline(admin.TabularInline):
    model = TeamMember
    extra = 4

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'author', 'created_at')

    fields = ('name', 'description', 'author', 'image', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    inlines = [
        OrderItemInline
    ]