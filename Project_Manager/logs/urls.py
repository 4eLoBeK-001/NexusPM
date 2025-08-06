from django.urls import include, path

from . import views

app_name = 'logs'

urlpatterns = [
    path('', views.history, name='history'),
    path('search/', views.history_search, name='history_search'),
    path('filter/', views.history_filter, name='history_filter'),

    path('team/<int:pk>/', views.team_history, name='team_history'),
    path('team/<int:pk>/project/<int:project_pk>/', views.project_history, name='project_history'),

]
