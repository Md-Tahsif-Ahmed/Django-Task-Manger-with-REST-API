from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, TaskForm
from django.contrib.auth.decorators import login_required

from django.views import View
from django.http import HttpResponse
from .models import Task
from django.contrib.auth.models import User

# User Authentication part
def sign_up(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect(reverse('tasks:task_list'))
    
    return render(request, 'tasks_auth/sign_up.html', {'form': form})

def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('tasks:task_list'))  # Redirect to the task list page
    
    return render(request, 'tasks_auth/sign_in.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('tasks:sign_in'))
# CRUD operation for task Manager
# @login_required
class TaskListView(View):
    template_name = 'tasks/task_list.html'

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        return render(request, self.template_name, {'tasks': tasks})
    
class TaskCreateView(View):
    template_name = 'tasks/task_create.html'

    def get(self, request):
        form = TaskForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect(reverse('tasks:task_list'))
        return render(request, self.template_name, {'form': form})

class TaskDetailView(View):
    template_name = 'tasks/task_detail.html'

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        if task.user == request.user:
            return render(request, self.template_name, {'task': task})
        else:
            return HttpResponse("You don't have permission to view this task.")

class TaskUpdateView(View):
    template_name = 'tasks/task_update.html'

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        if task.user == request.user:
            form = TaskForm(instance=task)
            return render(request, self.template_name, {'form': form, 'task': task})
        else:
            return HttpResponse("You don't have permission to edit this task.")

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        if task.user == request.user:
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect(reverse('tasks:task_list'))  # Redirect to the task list page
            return render(request, self.template_name, {'form': form, 'task': task})
        else:
            return HttpResponse("You don't have permission to edit this task.")
