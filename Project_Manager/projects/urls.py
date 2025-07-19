from django.urls import include, path

from decorator_include import decorator_include

from tasks.utils.decorators import require_project_member
from . import views

app_name = 'projects'

urlpatterns = [
    path('<int:team_pk>/project/', decorator_include(require_project_member, 'tasks.urls', namespace='tasks')),

    path('<int:pk>/projects/', views.project_list, name='project_list'),
    path('<int:pk>/search/', views.search_projects, name='search_team'),
    path('<int:pk>/project/<int:project_pk>/setting/', views.project_settings, name='project_settings'),
    
    path('<int:pk>/project/<int:project_pk>/members/', views.project_members, name='project_members'),
    path('<int:pk>/project/<int:project_pk>/members/add/', views.add_project_members, name='add_project_members'),
    path('<int:pk>/project/<int:project_pk>/members/search/', views.search_members, name='search_members'),
    path('<int:pk>/project/<int:project_pk>/member/<int:member_pk>/delete/', views.delete_project_members, name='delete_project_members'),
    
    path('<int:pk>/project/<int:project_pk>/tags/', views.project_tags, name='project_tags'),
    path('<int:pk>/project/<int:project_pk>/tag/delete/', views.delete_tag, name='delete_tag'),
    path('<int:pk>/project/<int:project_pk>/tag/search/', views.search_tags, name='search_tags'),
    path('<int:pk>/project/<int:project_pk>/tag/create/', views.create_tag, name='create_tag'),
    
    path('<int:pk>/project/<int:project_pk>/statuses/', views.project_statuses, name='project_statuses'),
    path('<int:pk>/project/<int:project_pk>/statuses/create/', views.create_status, name='create_status'),
    path('<int:pk>/project/<int:project_pk>/statuses/search/', views.search_status, name='search_status'),
    path('<int:pk>/project/<int:project_pk>/statuses/delete/', views.delete_status, name='delete_status'),

    path('create/', views.create_project, name='create_project'),
    path('delete/<int:project_pk>/', views.delete_project, name='delete_project'),
    path('change_status/<int:project_pk>/', views.project_status_changes, name='project_status_changes'),

]
