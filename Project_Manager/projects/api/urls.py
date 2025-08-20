from django.urls import include, path

from projects.api import views

app_name = 'projects'

urlpatterns = [
    path('project/<int:project_id>/', include('tasks.api.urls', namespace='tasks')),
    
    path('projects/', views.ProjectList.as_view(), name='project_list'),

    path('project/<int:project_id>/', include([
        path('', views.ProjectDetailAPIView.as_view(), name='project_detail'),
        path('members/', views.ProjectMembersAPIView.as_view(), name='project_members'),

        path('statuses/', views.ProjectStatusesAPIView.as_view(), name='project_statuses'),
        path('tags/', views.ProjectTagsAPIView.as_view(), name='project_tags'),
    ])),
]

