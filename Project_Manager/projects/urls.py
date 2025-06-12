from django.urls import include, path

from . import views

app_name = 'projects'

urlpatterns = [
    path('<int:team_pk>/project/', include('tasks.urls', namespace='tasks')),

    path('<int:pk>/projects/', views.project_list, name='project_list'),
    path('<int:pk>/search/', views.search_team, name='search_team'),
    path('<int:pk>/project/<int:project_pk>/setting/', views.project_settings, name='project_settings'),
    path('create/', views.create_project, name='create_project'),
    path('delete/<int:pk>/', views.delete_project, name='delete_project'),
    path('change_status/<int:pk>/', views.project_status_changes, name='project_status_changes'),

    path('list/', views.project_list_t, name='project_list_t'),
    path('lst/', views.project_lst, name='project_lst'),
    path('card/', views.project_card, name='project_card'),
]
