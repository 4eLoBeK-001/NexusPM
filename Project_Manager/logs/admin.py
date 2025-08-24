from django.contrib import admin

from logs.models import ActionLog

@admin.register(ActionLog)
class sas(admin.ModelAdmin):
    fields = ('user', 'team', 'project', 'task', 'action_type', 'data', 'created_at', 'participants')
    readonly_fields = ('created_at',)
