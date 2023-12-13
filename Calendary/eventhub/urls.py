from .views import CreateTagView, CreateTasksView, DeleteTasksView, ListTagsView, ListTasksView, TaskListView, UpdateTasksView, CalendarView
from django.urls import path

urlpatterns = [
    path("list_tasks/<int:year>/<int:month>/<int:day>/", ListTasksView.as_view(), name="list tasks"),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('calendar/<int:year>/<int:month>/', CalendarView.as_view(), name='calendar'),
    path("create_task/", CreateTasksView.as_view(), name="create task"),
    path("uptate_task/<int:pk>/", UpdateTasksView.as_view(), name="update task"),
    path("delete_task/<int:pk>/", DeleteTasksView.as_view(), name="delete task"),

    path("list_tags/", ListTagsView.as_view(), name="list tags"),
    path("create_tag/", CreateTagView.as_view(), name="create tag"),
]
