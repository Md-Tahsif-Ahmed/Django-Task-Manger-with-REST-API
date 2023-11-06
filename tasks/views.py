from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth import login
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

