from django.contrib import admin
from django.db.models import Count

from tasks.models import Task, Tag, Status, Color, Comment, TaskImage

# Register your models here.

class ExecutorsCountFilter(admin.SimpleListFilter):
    title = 'Кол-во исполнителей'
    parameter_name = 'executorsa'

    def lookups(self, request, model_admin):
        return (
            ('e_0', 'Нет исполнителей'),
            ('e_1>', 'Есть хотя бы один исполнителей'),
            ('e_5>', 'Исполнителей: ≥ 5'),
            ('e_15>', 'Исполнителей: ≥ 15'),
            ('e_30>', 'Исполнителей: ≥ 30'),
        )
    
    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset
        
        queryset = queryset.annotate(exec_count=Count('executor'))

        if value == 'e_0':
            return queryset.filter(exec_count=0)
        if value == 'e_1>':
            return queryset.filter(exec_count__gte=1)
        if value == 'e_5>':
            return queryset.filter(exec_count__gte=5)
        if value == 'e_15>':
            return queryset.filter(exec_count__gte=15)
        if value == 'e_30>':
            return queryset.filter(exec_count__gte=30)


class TagTabularInline(admin.TabularInline):
    model = Task.tag.through
    extra = 2
    max_num = 8
    classes = ('collapse',)

class ExecutorTabularInline(admin.TabularInline):
    model = Task.executor.through
    extra = 2
    max_num = 8
    classes = ('collapse',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'project', 'priority', 'created_at', 'updated_at')
    list_display_links = ('name', 'creator', 'project')
    ordering = ('-created_at',)
    list_filter = (ExecutorsCountFilter, 'priority', 'created_at',)
    search_fields = ('name', 'project__name', 'creator')

    fieldsets = (
        (None, {
            'fields': ('name', 'created_at', 'updated_at'),
        }),
        ('Общая информация', {
            'description': '<h1>Общая информация</h1>',
            'fields': ('description', 'creator', 'project', 'color', 'parent_task'),
        }),
        ('Прочая информация', {
            'description': '<h1>Теги, статусы и приоритет</h1>',
            'fields': ('tag', 'status', 'priority'),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ('created_at', 'updated_at')
    
    inlines = [
        TagTabularInline,
        ExecutorTabularInline
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'project')
    list_display_links = ('name', 'project')
    list_filter = ('name', 'project__name')
    search_fields = ('name', 'project__name')

    fields = ('name', 'project', 'color')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'is_completed', 'color')
    list_display_links = ('name', 'project')
    list_filter = ('is_completed', 'project__name')
    search_fields = ('name', 'project__name')
    
    fields = ('name', 'project', 'is_completed', 'color')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_name', 'bg_color', 'text_color', 'border_color')
    list_filter = ('name', 'color_name')
    search_fields = ('name', 'color_name')
    
    readonly_fields = ('name', 'color_name', 'bg_color', 'text_color', 'border_color')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'task', 'created_at')
    list_display_links = ('content', 'author', 'task')
    ordering = ('-created_at',)
    list_filter = ('content', 'author__username', 'task__name')
    search_fields = ('content', 'author__username', 'task__name')

    fields = ('content', 'author', 'task', 'created_at')
    readonly_fields = ('created_at',)

admin.site.register(TaskImage)