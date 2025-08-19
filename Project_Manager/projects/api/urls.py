from django.urls import include, path

from projects.api import views

app_name = 'projects'

urlpatterns = [
    path('team/<int:pk>/project/<int:project_id>/', include('tasks.api.urls', namespace='tasks')),
    
    path('team/<int:pk>/projects/', views.ProjectList.as_view(), name='project_list'),
    path('team/<int:pk>/project/<int:project_id>/', views.ProjectDetailAPIView.as_view(), name='project_detail'),
    path('team/<int:pk>/project/<int:project_id>/members/', views.ProjectMembersAPIView.as_view(), name='project_members'),

    path('team/<int:pk>/project/<int:project_id>/statuses/', views.ProjectStatusesAPIView.as_view(), name='project_statuses'),
    path('team/<int:pk>/project/<int:project_id>/tags/', views.ProjectTagsAPIView.as_view(), name='project_tags'),

]

