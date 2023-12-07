from .views import CreateTasksView, DeleteTasksView, ListTasksView, UpdateTasksView
from django.urls import path

urlpatterns = [
    path("list_tasks/", ListTasksView.as_view(), name="list tasks"),
    path("create_task/", CreateTasksView.as_view(), name="create task"),
    path("uptate_task/<int:pk>/", UpdateTasksView.as_view(), name="update task"),
    path("delete_task/<int:pk>/", DeleteTasksView.as_view(), name="delete task")
]
