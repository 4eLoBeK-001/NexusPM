from django.urls import path

from tasks.api import views

app_name = 'tasks'

urlpatterns = [
    path('tasks/', views.TaskListAPIView.as_view(),name='task_list')
]