from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm

def sign_up(request):
    form = RegistrationForm()
    registered = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user=form.save()
            registered=True


            return HttpResponseRedirect(reverse('tasks:sign_in'))
    
    return render(request, 'tasks/sign_up.html', context={'form':form})

def sign_in(request):
    form = AuthenticationForm
    if request.method =='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return render(request, 'homepage.html')
    return render(request, 'tasks/sign_in.html', context={'form':form})