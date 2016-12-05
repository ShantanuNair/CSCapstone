"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


from .forms import LoginForm, RegisterForm, UpdateForm
from .models import MyUser, Student, Teacher, Engineer

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
    form = UpdateForm(request.POST or None, instance=request.user)
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

def view_profile(request):
    #TODO: include bookmarks later in context

    #Get user from DB instead of using requests.user because it doesn't have is_teacher etc. fields.

    DBUser = MyUser.objects.filter(email=request.user.email)[0]
    userType = ""
    print(DBUser.is_engineer)
    if DBUser.is_teacher:
        userType = "Teacher"
    elif DBUser.is_student:
        userType = "Student"
    elif DBUser.is_engineer:
        userType = "engineer"

    context = {
        "userType" : userType,
        "user" : DBUser
    }
    return render(request, 'profile.html', context)