from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('<int:project_pk>/tasks/', views.task_list, name='task_list'),
    path('<int:project_pk>/task/<int:task_pk>/', views.task_detail, name='task_detail'),
    path('<int:project_pk>/task/<int:task_pk>/status/change/', views.change_status, name='change_status'),
    path('<int:project_pk>/task/<int:task_pk>/status/create/', views.create_status, name='create_status'),

    path('<int:project_pk>/task/<int:task_pk>/pchange/', views.change_priority, name='change_priority'),
    
]
