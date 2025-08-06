from django.urls import include, path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),

    path('task/create/', views.create_task, name='create_task'),
    path('tasks/search/', views.task_search, name='task_search'),
    path('tasks/filter/', views.task_filter, name='task_filter'),

    path('task/<int:task_pk>/', include([
        path('', views.task_detail, name='task_detail'),

        path('subtask/create/', views.create_subtask, name='create_subtask'),
        
        path('change/', views.change_task, name='change_task'),
        path('delete/', views.task_delete, name='task_delete'),

        path('status/change/', views.change_status, name='change_status'),
        path('tag/change/', views.change_tag, name='change_tag'),

        path('pchange/', views.change_priority, name='change_priority'),

        path('comment/add/', views.add_comment, name='add_comment'),
        path('comment/<int:comm_pk>/delete/', views.delete_comment, name='delete_comment'),

        path('test/', views.add_executors, name='add_executors'),

        path('image/add/', views.processing_image, name='processing_image'),
    ])),
    
    
]
