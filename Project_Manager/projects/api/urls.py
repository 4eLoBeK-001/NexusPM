from django.urls import include, path

from projects.api import views

app_name = 'projects'

urlpatterns = [
    path('team/<int:pk>/projects/', views.ProjectList.as_view(), name='project_list'),
]

