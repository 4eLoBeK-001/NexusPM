from django.urls import include, path

from . import views

app_name = 'projects'

urlpatterns = [
    path('project/', include('tasks.urls', namespace='tasks')),

    path('list/<int:pk>/', views.project_list, name='project_list'),
    path('search/<int:pk>/', views.search_team, name='search_team'),
    path('create/', views.create_project, name='create_project'),
    path('delete/<int:pk>/', views.delete_project, name='delete_project'),
    path('change_status/<int:pk>/', views.project_status_changes, name='project_status_changes'),

    path('list/', views.project_list_t, name='project_list_t'),
    path('lst/', views.project_lst, name='project_lst'),
    path('card/', views.project_card, name='project_card'),
]
