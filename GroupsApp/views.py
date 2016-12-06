"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from .forms import addMemForm, assignProjForm
from AuthenticationApp.models import MyUser

def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups' : groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')


def getMyGroups(request):
    if request.user.is_authenticated():
        groups_list = request.user.group_set.all()
        context = {
            'groups' : groups_list,
        }
        return render(request, 'mygroups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)

        context = {
            'group' : in_group,
            'userIsMember': is_member,
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
                new_group.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'groupformsuccess.html', context)
        else:
            form = forms.GroupForm()
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.add(request.user)
        in_group.save();
        request.user.group_set.add(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    
def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.remove(request.user)
        in_group.save();
        request.user.group_set.remove(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': False,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')

def addMem(request):
    if request.user.is_authenticated:
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        form = addMemForm(request.POST or None)
        if form.is_valid():
            email1 = form.cleaned_data['email']
            #TODO: Make sure email entered belongs to Student and not just MyUser
            usernames = MyUser.objects.filter(email=email1)
            if len(usernames) == 0:
                context = {
                    "form": form,
                    "page_name": "Add a Member",
                    "button_value": "Add",
                    "links": ["login"],
                    "group": in_group,
                }
                return render(request, 'groupAdd.html', context)
            username = usernames[0]
            in_group.members.add(username)
            in_group.save();
            username.group_set.add(in_group)
            username.save()
            context = {
                'group': in_group,
                'userIsMember': True,
            }
            #form.save()
            return render(request, 'group.html', context)
        context = {
            "form": form,
            "page_name": "Add a Member",
            "button_value": "Add",
            "links": ["login"],
            "group": in_group,
        }
        return render(request, 'groupAdd.html', context)
    return render(request, 'autherror.html')

def assignProj(request):
    if request.user.is_authenticated:
        group_name = request.GET.get('name', 'None')
        current_group = models.Group.objects.get(name__exact=group_name)
        form = assignProjForm(request.POST or None)
        if form.is_valid():
            selectedproj = form.cleaned_data['project']
            #Set projects and groups assignment to True
            selectedproj.is_assignedToGroup = True
            current_group.is_assignedToProject = True
            #Save proj so group can link to it
            selectedproj.save()
            current_group.project = selectedproj
            print(vars(current_group)) #DEBUGGING
            current_group.save()
            context = {
                'group': current_group,
                'userIsMember': True,
            }
            print() #DEBUGGING
            return render(request, 'group.html', context)

        context = {
            "form": form,
            "page_name": "Assign A Project",
            "button_value": "Assign Project",
            "links": ["login"],
            "group": current_group,
        }
        return render(request, 'groupAssignProj.html', context)

    return render(request, 'autherror.html')

#TODO: Build suggestions and matching for groups-projects
def suggestProj(request):
    pass

def leaveProj(request):
    if request.user.is_authenticated:
        group_name = request.GET.get('name', 'None')
        current_group = models.Group.objects.get(name__exact=group_name)

        changed_project = current_group.project
        #Set projects and groups assignment to False
        current_group.project_id = None
        current_group.is_assignedToProject = False
        changed_project.is_assignedToGroup = False
        #print(changed_project.assignedGroup) # DEBUGGING
        #print(vars(current_group))  # DEBUGGING
        #print(vars(changed_project))  # DEBUGGING
        #Save proj so group can link to it
        changed_project.save()
        current_group.save()
        context = {
            'group': current_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)


    return render(request, 'autherror.html')
