"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from .forms import addMemForm, assignProjForm
from AuthenticationApp.models import MyUser, Student
from ProjectsApp.models import Project

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

        current_group = models.Group.objects.get(name__exact=in_group)
        members_list = current_group.members.all()
        stud = []
        for member in members_list:
            stu = Student.objects.get(user=member)

            skills = stu.knownLanguages
            if skills not in stud:
                stud.append(skills)
        print(stud)
        context = {
            'group' : in_group,
            'userIsMember': is_member,
            'student' : stud,
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

        current_group = models.Group.objects.get(name__exact=in_group)
        members_list = current_group.members.all()
        stud = []
        for member in members_list:
            stu = Student.objects.get(user=member)
            skills = stu.knownLanguages
            if skills not in stud:
                stud.append(skills)

        context = {
            'group' : in_group,
            'userIsMember': True,
            'student':stud,
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

        current_group = models.Group.objects.get(name__exact=in_group)
        members_list = current_group.members.all()
        stud = []
        for member in members_list:
            stu = Student.objects.get(user=member)
            skills = stu.knownLanguages
            if skills not in stud:
                stud.append(skills)
        context = {
            'group' : in_group,
            'userIsMember': False,
            'student' : stud,
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

            current_group = models.Group.objects.get(name__exact=in_group)
            members_list = current_group.members.all()
            stud = []
            for member in members_list:
                stu = Student.objects.get(user=member)
                skills = stu.knownLanguages
                if skills not in stud:
                    stud.append(skills)

            context = {
                'group': in_group,
                'userIsMember': True,
                'student':stud,
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
            curr_group = models.Group.objects.get(name__exact=group_name)
            members_list = curr_group.members.all()
            stud = []
            for member in members_list:
                stu = Student.objects.get(user=member)

                skills = stu.knownLanguages
                if skills not in stud:
                    stud.append(skills)
            context = {
                'group': current_group,
                'userIsMember': True,
                'student':stud,
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
    projects_list = models.Project.objects.all()
    print(projects_list)
    group_name = request.GET.get('name', 'None')
    current_group = models.Group.objects.get(name__exact=group_name)
    members_list = current_group.members.all()
    skill_list = []
    yearsTot = 0
    c = 0
    for member in members_list:
        stu = Student.objects.get(user = member)
        skills = stu.knownLanguages.split(',')
        for skill in skills:
            if skill not in skill_list:
                skill_list.append(skill)

        sskills = stu.experience
        if sskills!=None:
            yearsTot= yearsTot + int(sskills)
        c=c+1
    print("The years list is")
    print(yearsTot/c)

    suggestedProj = []

    for projects in projects_list:
        project = Project.objects.get(name = projects)
        skillsreqd = project.language
        if skillsreqd != None:
            skillsreqd = skillsreqd.split(',')
            print(skillsreqd)
            flag = True
            for skill in skillsreqd:
                if skill not in skill_list:
                    flag = False

            if flag == True:
                if project not in suggestedProj and float(yearsTot/c)>float(project.experience):
                    suggestedProj.append(project)
    print (suggestedProj)
   # for project in projects_list:

    return render(request, 'SuggestedProjects.html', {
        'projects': suggestedProj,
        'group_name':group_name,
    })


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

        curr_name = models.Group.objects.get(name__exact=group_name)
        members_list = curr_name.members.all()
        stud = []
        for member in members_list:
            stu = Student.objects.get(user=member)
            skills = stu.knownLanguages
            if skills not in stud:
                stud.append(skills)

        context = {
            'group': current_group,
            'userIsMember': True,
            'student':stud,

        }
        return render(request, 'group.html', context)


    return render(request, 'autherror.html')

