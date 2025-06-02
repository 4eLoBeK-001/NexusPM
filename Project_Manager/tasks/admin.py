from django.contrib import admin

from tasks.models import Task, Tag, TagColor

# Register your models here.

admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(TagColor)