from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, TaskForm
from django.contrib.auth.decorators import login_required

from django.views import View
from django.http import HttpResponse
from .models import Task
from django.contrib.auth.models import User

# For API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Photo
from .serializers import TaskSerializer, PhotoSerializer
 
 

def home(request):
    return render(request, 'homepage.html')

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
    return render(request, 'homepage.html')
# CRUD operation for task Manager
# @login_required
 
class TaskListView(View):
    template_name = 'tasks/task_list.html'

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)

        # Get query parameters from the URL
        query = request.GET.get('q')
        filter_priority = request.GET.get('priority')
        filter_completed = request.GET.get('completed')

        # Apply filters and search
        if query:
            tasks = tasks.filter(title__icontains=query) | tasks.filter(description__icontains=query)
        if filter_priority:
            tasks = tasks.filter(priority=filter_priority)
        if filter_completed:
            tasks = tasks.filter(is_complete=True if filter_completed == 'true' else False)

        return render(request, self.template_name, {'tasks': tasks})

class TaskCreateView(View):
    template_name = 'tasks/task_create.html'

    def get(self, request):
        form = TaskForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TaskForm(request.POST, request.FILES)
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



class TaskDeleteView(View):
    template_name = 'tasks/task_delete.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.user == request.user:
            return render(request, self.template_name, {'task': task})
        else:
            return HttpResponse("You don't have permission to delete this task.")

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.user == request.user:
            task.delete()
            return redirect(reverse('tasks:task_list'))
        else:
            return HttpResponse("You don't have permission to delete this task.")
# API Part

class TaskList(APIView):
    """
    List all tasks and create a new task
    """

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    """
    Detail, update, delete Tasks
    """

    def get_object(self, pk):
        try:
            task = Task.objects.get(pk=pk)
            return task
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
