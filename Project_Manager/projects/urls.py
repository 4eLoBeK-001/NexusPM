from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.main_page, name='home'),
    path('list/<int:pk>/', views.project_list, name='project_list'),
    path('lst/', views.project_lst, name='project_lst'),
    path('card/', views.project_card, name='project_card'),
]
