from django.contrib import admin

from .models import Project
# Register your models here.





@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'team', 'created_at', 'updated_at')
    list_display_links = ('name', 'team')