from django.urls import include, path

from tasks.api import views

app_name = 'tasks'

urlpatterns = [
    path('tasks/', views.TaskListAPIView.as_view(),name='task_list'),
    path('task/<int:task_id>/', include([
        path('', views.TaskDetailAPIView.as_view(),name='task_detail'),
        path('comments/', views.CommentListAPIView.as_view(),name='comment_list'),
        path('comment/<int:comment_id>/', views.CommentDeleteAPIView.as_view(),name='comment_delete'),
    ])),
]