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
    pass


@login_required(login_url='login')
def materials(request):
    pass


@login_required(login_url='login')
def projects(request):
    pass


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
def logout(request):
    pass


def login(request):
    return render(request, 'projectcalculator/login.html', {
        'login_form': LoginForm()
    })


def register(request):
    return render(request, 'projectcalculator/register.html', {
        'register_form': RegisterForm()
    })