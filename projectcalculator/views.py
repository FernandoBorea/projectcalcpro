from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import *

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'projectcalculator/index.html')


@login_required(login_url='login')
def materials(request):

    if request.method == 'POST':
        material_form = MaterialForm(request.POST)

        if material_form.is_valid():
            # This takes form instance into a model instance
            new_material = material_form.save(commit=False)

            # Fill missing fields that aren't present in form and save
            new_material.created_by = request.user
            new_material.save()

            return HttpResponseRedirect(reverse('materials'))

    materials = Material.objects.filter(created_by=request.user).order_by('created_on')
    paginator = Paginator(materials, 9)

    # Check if we got a valid page GET argument
    requested_page = request.GET.get('page', '1')

    try:
        requested_page = int(requested_page)
    except ValueError:
        return HttpResponseRedirect(reverse('materials'))
    
    if requested_page > paginator.num_pages:
        return HttpResponseRedirect(reverse('materials'))
    
    # If we don't have any errors, return requested page
    page_obj = paginator.get_page(requested_page)
    page_range = paginator.page_range

    return render(request, 'projectcalculator/materials.html', {
        'material_form': MaterialForm(),
        'materials_page_obj': page_obj,
        'paginator_range': page_range
    })


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