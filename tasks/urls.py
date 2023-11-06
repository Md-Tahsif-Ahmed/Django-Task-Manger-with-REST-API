from django.urls import path
from tasks import views

app_name = "tasks"

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
      
]