from django.urls import include, path

from . import views

app_name = 'logs'

urlpatterns = [
    path('', views.history, name='history'),
    path('search/', views.history_search, name='history_search'),
    path('filter/', views.history_filter, name='history_filter'),
]
