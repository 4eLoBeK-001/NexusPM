from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('<int:project_pk>/tasks/', views.task_list, name='task_list'),
    path('<int:project_pk>/task/create/', views.create_task, name='create_task'),
    path('<int:project_pk>/task/<int:task_pk>/subtask/create/', views.create_subtask, name='create_subtask'),
    path('<int:project_pk>/task/<int:task_pk>/', views.task_detail, name='task_detail'),
    path('<int:project_pk>/task/<int:task_pk>/delete/', views.task_delete, name='task_delete'),

    path('<int:project_pk>/tasks/search/', views.task_search, name='task_search'),
    path('<int:project_pk>/tasks/filter/', views.task_filter, name='task_filter'),

    path('<int:project_pk>/task/<int:task_pk>/status/change/', views.change_status, name='change_status'),
    path('<int:project_pk>/task/<int:task_pk>/status/create/', views.create_status, name='create_status'),

    path('<int:project_pk>/task/<int:task_pk>/pchange/', views.change_priority, name='change_priority'),

    path('<int:project_pk>/task/<int:task_pk>/comment/add/', views.add_comment, name='add_comment'),
    path('<int:project_pk>/task/<int:task_pk>/comment/<int:comm_pk>/delete/', views.delete_comment, name='delete_comment'),

    path('<int:project_pk>/task/<int:task_pk>/test/', views.add_executors, name='add_executors'),
    
]
