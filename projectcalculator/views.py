from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import *

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'projectcalculator/index.html')


@login_required(login_url='login')
def materials(request):
    return render(request, 'projectcalculator/materials.html')


@login_required(login_url='login')
def projects(request):
    return render(request, 'projectcalculator/projects.html')


@login_required(login_url='saved_projects')
def saved_projects(request):
    pass


@login_required(login_url='login')
def project(request, project_id):
    pass


@login_required(login_url='login')
def profile(request):
    pass


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def login_view(request):

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['email'], password=login_form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            
            return render(request, 'projectcalculator/login.html', {
                'message': 'Invalid credentials',
                'login_form': LoginForm()
            })
    
    return render(request, 'projectcalculator/login.html', {
        'login_form': LoginForm()
    })


def register(request):

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():

            password = register_form.cleaned_data['password']
            confirmation = register_form.cleaned_data['password_confirmation']

            if password != confirmation:
                return render(request, 'projectcalculator/register.html', {
                    'message': 'Password and confirmation doesn\'t match',
                    'register_form': RegisterForm()
                })

            username = register_form.cleaned_data['email']
            email = register_form.cleaned_data['email']

            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, 'projectcalculator/register.html', {
                    'message': 'Email already taken',
                    'register_form': RegisterForm()
                })
            
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'projectcalculator/register.html', {
        'register_form': RegisterForm()
    })