from django.contrib import admin

from tasks.models import Task, Tag, Status, Color, Comment

# Register your models here.

admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(Status)
admin.site.register(Color)
admin.site.register(Comment)