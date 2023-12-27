from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import *
from django.db.models import F, Value
import json

# Create your views here.
@login_required(login_url='login')
def index(request):

    projects = request.user.saved_projects.all()
    paginator = Paginator(projects, 9)

    # Check if we got a valid page GET argument
    requested_page = request.GET.get('page', '1')
    
    try:
        requested_page = int(requested_page)
    except ValueError:
        return HttpResponseRedirect(reverse('projects'))
    
    if requested_page > paginator.num_pages:
        return HttpResponseRedirect(reverse('projects'))
    
    # If we don't have any errors, return requested page
    page_obj = paginator.get_page(requested_page)
    page_range = paginator.page_range

    return render(request, 'projectcalculator/index.html', {
        'projects_page_obj': page_obj,
        'paginator_range': page_range
    })


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

    if request.method == 'POST':

        # print(f'Request object: {request}')
        # print(f'POST info: {request.POST}')

        # Process formset
        formset = ProjectMaterialSetFormSet(request.POST, prefix='proj-mats')
        project_form = ProjectMaterialSetFormSet.ProjectForm(request.POST, prefix='proj-mats')

        if not project_form.is_valid():
             print('Project Form Errors:', project_form.errors) # Project Form Errors: <ul class="errorlist"><li>name<ul class="errorlist"><li>This field is required.</li></ul></li></ul>

        if formset.is_valid():
            # print('Valid form')
            formset.save(request.user)
        # else:
        #     print(f'Invalid form, errors: {formset.errors}')
        #     print(formset.non_form_errors())


    projects = Project.objects.filter(created_by=request.user).order_by('created_on')
    paginator = Paginator(projects, 9)

    # Check if we got a valid page GET argument
    requested_page = request.GET.get('page', '1')
    
    try:
        requested_page = int(requested_page)
    except ValueError:
        return HttpResponseRedirect(reverse('projects'))
    
    if requested_page > paginator.num_pages:
        return HttpResponseRedirect(reverse('projects'))
    
    # If we don't have any errors, return requested page
    page_obj = paginator.get_page(requested_page)
    page_range = paginator.page_range

    # Research this
    initial = Material.objects.values(material=F('id'), material_name=F('name')).annotate(DELETE=Value(True))
    formset = ProjectMaterialSetFormSet(initial=initial, prefix='proj-mats')
    # Not so sure about why minus 1 here. I did it 
    # in my code. Remove it if you find problem. 
    # Nando: Probably it's starting at index 0
    formset.extra = len(initial) - 1
   
    return render(request, 'projectcalculator/projects.html', {
        'projects_page_obj': page_obj,
        'paginator_range': page_range,
        'formset': formset
    })


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

def delete_material(request):
    
    if request.method == 'DELETE':
        material_id = json.loads(request.body)['material_id']
        material = Material.objects.get(pk=material_id)
        material.delete()

        return JsonResponse({
            'delete_response': True
        }, status=200)

    return JsonResponse({
        'error': 'Invalid method'
    }, status=405)

        

def delete_project(request):
    
    if request.method == 'DELETE':
        project_id = json.loads(request.body)['project_id']
        project = Project.objects.get(pk=project_id)
        project.delete()

        return JsonResponse({
            'delete_response': True
        }, status=200)

    return JsonResponse({
        'error': 'Invalid method'
    }, status=405)


def edit_material(request, material_id):

    material = Material.objects.get(pk=material_id)

    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('materials'))
        
        return render(request, 'projectcalculator/edit_material.html', {
            'material_form': form,
            'message': 'Invalid edit'
        })
    
    material_form = MaterialForm(instance=material)

    return render(request, 'projectcalculator/edit_material.html', {
        'material_form': material_form
    })

def save_project(request, project_id):

    user = request.user
    project = Project.objects.get(pk=project_id)
    user.saved_projects.add(project)