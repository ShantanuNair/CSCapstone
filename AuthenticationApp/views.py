"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


from .forms import LoginForm, RegisterForm, UpdateForm,updateEngineer, updateTeacher,updateStudent
from .models import MyUser, Student, Teacher, Engineer
from ProjectsApp.models import Project
from GroupsApp.models import Group

# Auth Views

def auth_login(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next')
    if next_url is None:
        next_url = "/"
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            messages.success(request, 'Success! Welcome, '+(user.first_name or ""))
            login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            messages.warning(request, 'Invalid username or password.')

    context = {
        "form": form,
        "page_name" : "Login",
        "button_value" : "Login",
        "links" : ["register"],
    }
    return render(request, 'auth_form.html', context)

def auth_logout(request):
    logout(request)
    messages.success(request, 'Success, you are now logged out')
    return render(request, 'index.html')

def auth_register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        usertype = form.cleaned_data['usertype']
        if usertype == 'Teacher':
            new_user = MyUser.objects.create_user(email=form.cleaned_data['email'],
                password=form.cleaned_data['password2'],
                first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'])
            new_user.is_teacher = True
            new_user.save()
            new_teacher = Teacher(teacher=new_user, university=form.cleaned_data['university'])
            new_teacher.about = form.cleaned_data['about']
            new_teacher.save()
            login(request, new_user);
            messages.success(request, 'Success! Your (Teacher) account was created.')
            return render(request, 'index.html')
        elif usertype == 'Engineer':
            new_user = MyUser.objects.create_user(email=form.cleaned_data['email'],
                                                  password=form.cleaned_data['password2'],
                                                  first_name=form.cleaned_data['firstname'],
                                                  last_name=form.cleaned_data['lastname'])
            new_user.is_engineer = True
            new_user.save()
            new_engineer = Engineer(engineer=new_user, company=form.cleaned_data['company'], almamater=form.cleaned_data['university'])
            new_engineer.about = form.cleaned_data['about']
            new_engineer.save()
            login(request, new_user);
            messages.success(request, 'Success! Your (Engineer) account was created.')
            return render(request, 'index.html')
        elif usertype == 'Student':
            new_user = MyUser.objects.create_user(email=form.cleaned_data['email'],
                                                  password=form.cleaned_data['password2'],
                                                  first_name=form.cleaned_data['firstname'],
                                                  last_name=form.cleaned_data['lastname'])
            new_user.is_student = True
            new_user.save()
            new_student = Student(user=new_user, university=form.cleaned_data['university'])
            new_student.about = form.cleaned_data['about']
            new_student.knownLanguages = form.cleaned_data['knownLanguagesText']
            new_student.experience = form.cleaned_data['experience']
            new_student.specialty = form.cleaned_data['specialty']
            new_student.save()
            login(request, new_user);
            messages.success(request, 'Success! Your (Student) account was created.')
            return render(request, 'index.html')
    context = {
        "form": form,
        "page_name" : "Register",
        "button_value" : "Register",
        "links" : ["login"],
    }
    return render(request, 'auth_form.html', context)

@login_required
def update_profile(request):
    form = RegisterForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Success, your profile was saved!')

    context = {
        "form": form,
        "page_name" : "Update",
        "button_value" : "Update",
        "links" : ["logout"],
    }
    return render(request, 'auth_form.html', context)

def updateSubUser(request):

    usertype = ""
    #form = updateEngineer(request.POST or None)
    form = None
    if request.user.is_teacher:
        form = updateTeacher(request.POST or None)
    if request.user.is_engineer:
        form = updateEngineer(request.POST or None)
    if request.user.is_student:
        form = updateStudent(request.POST or None)

    if form.is_valid():
        if request.user.is_teacher:
            usertype = 'Teacher'
        if request.user.is_engineer:
            usertype = 'Engineer'
        if request.user.is_student:
            usertype = 'Student'
        #usertype = form.cleaned_data['usertype']
        if usertype == 'Teacher':
            if form.cleaned_data['firstname'] != "":
                request.user.first_name = form.cleaned_data['firstname']
            if form.cleaned_data['lastname'] != "":
                request.user.last_name = form.cleaned_data['lastname']
            request.user.save()
            toUpdate_teacher = Teacher.objects.get(teacher=request.user)#(teacher=new_user, university=form.cleaned_data['university'])
            #if form.cleaned_data['university'] != None:
              #  toUpdate_teacher.university = form.cleaned_data['university']
            if form.cleaned_data['about'] != "":
                toUpdate_teacher.about = form.cleaned_data['about']
            toUpdate_teacher.save()
            messages.success(request, 'Success! Your (Teacher) account was updated.')
            return render(request, 'index.html')
        elif usertype == 'Engineer':
            if form.cleaned_data['firstname'] != "":
                request.user.first_name = form.cleaned_data['firstname']
            if form.cleaned_data['lastname'] != "":
                request.user.last_name = form.cleaned_data['lastname']
            request.user.save()
            toUpdate_engineer = Engineer.objects.get(engineer = request.user)#(engineer=new_user, company=form.cleaned_data['company'], almamater=form.cleaned_data['university'])
            if form.cleaned_data['about'] != "":
                toUpdate_engineer.about = form.cleaned_data['about']
            toUpdate_engineer.save()
            messages.success(request, 'Success! Your (Engineer) account was updated.')
            return render(request, 'index.html')
        elif usertype == 'Student':
            if form.cleaned_data['firstname'] != "":
                request.user.first_name = form.cleaned_data['firstname']
            if form.cleaned_data['lastname'] != "":
                request.user.last_name = form.cleaned_data['lastname']
            request.user.save()
            #new_student = Student(user=new_user, university=form.cleaned_data['university'])

            toUpdate_Student = Student.objects.get(user=request.user)
            #if form.cleaned_data['university'] != None:
                #toUpdate_Student.university = form.cleaned_data['university']
            if form.cleaned_data['about'] != "":
                toUpdate_Student.about = form.cleaned_data['about']
            if form.cleaned_data['knownLanguagesText'] != "":
                toUpdate_Student.knownLanguages = form.cleaned_data['knownLanguagesText']
            if form.cleaned_data['experience'] != "":
                toUpdate_Student.experience = form.cleaned_data['experience']
            if form.cleaned_data['specialty'] != "":
                toUpdate_Student.specialty = form.cleaned_data['specialty']

            toUpdate_Student.save()
           # login(request, new_user);
            messages.success(request, 'Success! Your (Student) account was updated.')
            return render(request, 'index.html')
    context = {
        "form": form,
        "page_name" : "Update",
        "button_value" : "Update",
        "links" : ["login"],
    }
    return render(request, 'auth_form.html', context)

def view_profile(request):
    #TODO: include bookmarks later in context

    #Get user from DB instead of using requests.user because it doesn't have is_teacher etc. fields.

    DBUser = MyUser.objects.filter(email=request.user.email)[0]
    SubUser = None
    userType = ""
    groups_list = None
    if DBUser.is_teacher:
        userType = "Teacher"
        SubUser = Teacher.objects.get(teacher=DBUser)
    elif DBUser.is_student:
        userType = "Student"
        groups_list = request.user.group_set.all()
        SubUser = Student.objects.get(user=DBUser)
    elif DBUser.is_engineer:
        userType = "engineer"
        SubUser = Engineer.objects.get(engineer=DBUser)

    context = {
        "userType" : userType,
        "user" : DBUser,
        "groups": groups_list,
        "SubUser":SubUser,
    }
    return render(request, 'profile.html', context)

def view_studentProfile(request):
    #TODO: include bookmarks later in context

    #Get user from DB instead of using requests.user because it doesn't have is_teacher etc. fields.

    studentEmail = request.GET.get('email', 'None')
    DBMyUser = MyUser.objects.filter(email=studentEmail)[0]
    DBUser = Student.objects.get(user=DBMyUser)
    userType = ""
    groups_list = None
    if DBMyUser.is_teacher:
        userType = "Teacher"
    elif DBMyUser.is_student:
        userType = "Student"
        groups_list = DBMyUser.group_set.all()
    elif DBMyUser.is_engineer:
        userType = "engineer"

    context = {
        "userType" : userType,
        "user" : DBMyUser,
        "student": DBUser,
        "groups": groups_list
    }
    return render(request, 'studentProfile.html', context)

def view_bookmarks(request):

    tableText = "Here are your bookmarked projects"

    context = {
        "user" : request.user,
        "bookmarks": request.user.bookmarks.all(),
        "tableText": tableText
    }
    return render(request, 'bookmarks.html', context)

def add_bookmark(request):
    if request.user.is_authenticated():
        projectName= request.GET.get('name', 'None')
        project = Project.objects.get(name=projectName)
        request.user.bookmarks.add(project)
        request.user.save()

        #Redirect to bookmarks page.
        tableText = "Here are your bookmarked projects"
        context = {
            "user": request.user,
            "bookmarks": request.user.bookmarks.all(),
            "tableText": tableText
        }
        return render(request, 'bookmarks.html', context)

    return render(request, 'autherror.html')

def remove_bookmark(request):
    if request.user.is_authenticated():
        projectName= request.GET.get('name', 'None')
        project = Project.objects.get(name=projectName)
        request.user.bookmarks.remove(project)
        request.user.save()

        #Redirect to bookmarks page.
        tableText = "Here are your bookmarked projects"
        context = {
            "user": request.user,
            "bookmarks": request.user.bookmarks.all(),
            "tableText": tableText
        }
        return render(request, 'bookmarks.html', context)

    return render(request, 'autherror.html')
