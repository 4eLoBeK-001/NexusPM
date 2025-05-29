from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('list/', views.task_list, name='task_list'),

]
