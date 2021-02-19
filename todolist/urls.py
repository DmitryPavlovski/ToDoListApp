from django.urls import path
from . import views
from .Views import TaskListView, UpdateTaskView, DeleteTaskView, CompleteTaskView, SignUpView

urlpatterns = [
    path('', TaskListView.TaskListView.as_view(), name="main"),
    path('index/', TaskListView.TaskListView.as_view(), name='index'),
    path("update/<int:pk>/", UpdateTaskView.UpdateTaskView.as_view(), name="update_task"),
    path("delete/<int:pk>/", DeleteTaskView.DeleteTaskView.as_view(), name="delete_task"),
    path("complete/<int:pk>/",CompleteTaskView.CompleteTaskView.as_view(), name="complete_task"),
    path('sign_up/', SignUpView.SignUpView.as_view(), name="sign_up")
]
