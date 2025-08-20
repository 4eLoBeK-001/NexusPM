from django.urls import include, path

from logs.api import views



urlpatterns = [
    path('logs/', views.LogActionsAPIView.as_view(),name='log_list'),
]