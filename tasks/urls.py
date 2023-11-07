from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
     path('', views.home, name='home'),
    path('signup/', views.sign_up, name='sign_up'),
    path('signin/', views.sign_in, name='sign_in'),
    path('signout/', views.sign_out, name='sign_out'),
    path('task-list/', views.TaskListView.as_view(), name='task_list'),
    path('create/', views.TaskCreateView.as_view(), name='create-task'),
    path('detail/<pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('update/<pk>/', views.TaskUpdateView.as_view(), name='update-task'),
    path('delete/<pk>', views.TaskDeleteView.as_view(), name='delete-task'),
]



