from django.urls import include, path
from django.contrib.auth.decorators import login_required

from decorator_include import decorator_include

from tasks.utils.decorators import require_project_member
from . import views
from tasks import views as tviews

app_name = 'projects'

urlpatterns = [
    path('project/<int:project_pk>/', 
         decorator_include(
            [login_required, require_project_member], 
            'tasks.urls', 
            namespace='tasks'
            )
        ),

    path('projects/', views.project_list, name='project_list'),

    path('search/', views.search_projects, name='search_team'),
    
    path('project/<int:project_pk>/', include([
        path('setting/', views.project_settings, name='project_settings'),
       
        path('members/', views.project_members, name='project_members'),
        path('members/add/', views.add_project_members, name='add_project_members'),
        path('members/search/', views.search_members, name='search_members'),
        path('member/<int:member_pk>/delete/', views.delete_project_members, name='delete_project_members'),
        
        path('tags/', views.project_tags, name='project_tags'),
        path('tag/delete/', views.delete_tag, name='delete_tag'),
        path('tag/search/', views.search_tags, name='search_tags'),
        path('tag/create/', views.create_tag, name='create_tag'),
        
        path('statuses/', views.project_statuses, name='project_statuses'),
        path('statuses/create/', views.create_status, name='create_status'),
        path('statuses/search/', views.search_status, name='search_status'),
        path('statuses/delete/', views.delete_status, name='delete_status'),
        path('change/', views.change_project, name='change_project'),
        path('delete/', views.delete_project, name='delete_project'),
        path('change_status/', views.project_status_changes, name='project_status_changes'),

    ])),

    path('create/', views.create_project, name='create_project'),
    
]
