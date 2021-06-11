from django.shortcuts import render

# Create your views here.

from django.shortcuts import  render, redirect
from .forms import ReportUserForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def signup(request):
    if request.method == 'POST':
        form = ReportUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful.' )
            return redirect('/')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    form = ReportUserForm
    return render (request=request, template_name='accounts/signup.html', context={'signup_form':form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('/')
            else:
                messages.error(request,'Invalid username or password.')
        else:
            messages.error(request,'Invalid username or password.')
    form = AuthenticationForm()
    return render(request=request, template_name='accounts/login.html', context={'login_form':form})

def logout(request):
    auth_logout(request)
    messages.info(request, 'Logout successfully')
    return redirect('/')