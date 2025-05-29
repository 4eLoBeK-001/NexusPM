from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('<int:project_pk>/tasks/', views.task_list, name='task_list'),

]
