from django.contrib import admin

from .models import Team

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = Team.team_member.through
    extra = 4

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'author', 'created_at')

    fields = ('name', 'description', 'author', 'image', 'created_at', 'updated_at')
    readonly_fields = ('team_member', 'created_at', 'updated_at')

    inlines = [
        OrderItemInline
    ]