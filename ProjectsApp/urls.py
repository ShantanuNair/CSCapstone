"""ProjectsApp URL Configuration

Created by Harris Christiansen on 10/02/16.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^project/all$', views.getProjects, name='Projects'),
    url(r'^project$', views.getProject, name='Project'),
    url(r'^project/form$', views.getProjectForm, name='ProjectForm'),
    url(r'^project/formsuccess$', views.getProjectFormSuccess, name='ProjectFormSuccess'),
    url(r'^project/companyProjects$', views.getCompanyProjects, name='PCompanyProjects'),
    url(r'^suggestedproject$', views.getSuggestedProjects, name='SuggestedProject'),
    url(r'^project/update', views.getUpdateProjectForm, name='UpdateProjectForm'),
    url(r'^project/remove', views.removeProject, name='removeProject'),
]