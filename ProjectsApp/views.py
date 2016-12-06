"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render
from . import forms

from . import models

def getProjects(request):
	projects_list = models.Project.objects.all()
	return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProject(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_project = models.Project.objects.get(name__exact=in_name)
        #is_member = in_project.members.filter(email__exact=request.user.email)

        context = {
            'project': in_project,
            #'userIsMember': is_member,
        }
        return render(request, 'project.html', context)
        # render error page if user is not logged in
    return render(request, 'autherror.html')


def getProjectForm(request):
    if request.user.is_authenticated():
        return render(request, 'projectform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getProjectFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.ProjectForm(request.POST)
            if form.is_valid():
                if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'projectform.html', {'error' : 'Error: That Project name already exists!'})
                new_project = models.Project(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
                new_project.language = form.cleaned_data['skills']
                new_project.experience = form.cleaned_data['experience']
                new_project.specialty = form.cleaned_data['specialty']
                new_project.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'projectformsuccess.html', context)
        else:
            form = forms.ProjectForm()
        return render(request, 'projectform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')