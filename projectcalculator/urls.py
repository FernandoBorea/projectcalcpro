from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('materials', views.materials, name='materials'),
    path('projects', views.projects, name='projects'),
    path('project/<int:project_id>', views.project, name='project'),
    path('saved_projects', views.saved_projects, name='saved_projects'),
    path('profile', views.profile, name='profile')
]