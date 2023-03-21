from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login

from django.http import HttpResponse

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,'Username or password is incorrect')

    return render(request, 'users/login.html')

def register_view(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            messages.success(request, 'Account was created for ' + form.cleaned_data.get('username'))
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])

            login(request, user)
            return redirect('dashboard')

        
    context = {'form': form}

    return render(request, 'users/register.html', context)