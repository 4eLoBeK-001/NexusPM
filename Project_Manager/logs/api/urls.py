from django.urls import include, path

from logs.api import views



urlpatterns = [
    path('logs/', views.LogActionsAPIView.as_view(),name='log_list'),
    path('logs/team/<int:pk>/', views.TeamHistoryAPIView.as_view(),name='history_team_list'),
    path('logs/team/<int:pk>/project/<int:project_id>/', views.ProjectHistoryAPIView.as_view(),name='history_project_list'),
]