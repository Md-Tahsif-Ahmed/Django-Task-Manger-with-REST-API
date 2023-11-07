from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tasks.models import Task

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

 


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'photos', 'priority', 'is_complete']

