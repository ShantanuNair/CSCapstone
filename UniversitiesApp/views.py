"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from AuthenticationApp.models import Teacher, MyUser
from UniversitiesApp.models import Course

def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember': is_member,
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityForm(request):
    if request.user.is_authenticated():
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
                new_university = models.University(name=form.cleaned_data['name'],
                                             photo=request.FILES['photo'],
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'universityformsuccess.html', context)
            else:
                return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.add(request.user)
        in_university.save();
        request.user.university_set.add(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': True,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')

def unjoinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.remove(request.user)
        in_university.save();
        request.user.university_set.remove(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': False,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')

def getCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        is_member = in_course.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse' : is_member,
        }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def courseForm(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        context = {
            'university': in_university,
        }
        return render(request, 'courseform.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def addCourse(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.CourseForm(request.POST)
            if form.is_valid():
                in_university_name = request.GET.get('name', 'None')
                in_university = models.University.objects.get(name__exact=in_university_name)
                if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
                    return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
                new_course = models.Course(tag=form.cleaned_data['tag'],
                                           name=form.cleaned_data['name'],
                                           description=form.cleaned_data['description'],
                                           university=in_university)
                new_course.save()
                in_university.course_set.add(new_course)
                is_member = in_university.members.filter(email__exact=request.user.email)
                context = {
                    'university' : in_university,
                    'userIsMember': is_member,
                }
                return render(request, 'university.html', context)
            else:
                return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
        else:
            form = forms.CourseForm()
            return render(request, 'courseform.html')
        # render error page if user is not logged in
    return render(request, 'autherror.html')

def removeCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.delete()
        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember' : is_member,
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.members.add(request.user)
        in_course.save();
        request.user.course_set.add(in_course)
        request.user.save()
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': True,
        }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def unjoinCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.members.remove(request.user)
        in_course.save();
        request.user.course_set.remove(in_course)
        request.user.save()
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': False,
        }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def getMyCourses(request):
    if request.user.is_authenticated():
        teacher= Teacher.objects.get(teacher=request.user)
        #in_name = request.GET.get('name', 'None')
        #in_university = models.University.objects.get(name__exact=in_name)
        #is_member = in_university.members.filter(email__exact=request.user.email)
        teacher_course_list = teacher.course_set.all()
        context = {
            'courseList' : teacher_course_list
        }
        return render(request, 'mycourses.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')


def getCourse2(request):
    if request.user.is_authenticated():
        course_tag = request.GET.get('name', 'None')
        course = Course.objects.get(tag=course_tag)
        context = {
            'course': course,
        }
        return render(request, 'course2.html', context)
    return render(request, 'autherror.html')


def addCourse2(request):
    if request.user.is_authenticated():

        form = forms.CourseForm(request.POST or None)
        if form.is_valid():
            current_teacher = Teacher.objects.get(teacher=request.user)
            in_university = current_teacher.university
            new_course = models.Course(tag=form.cleaned_data['tag'],
                                       name=form.cleaned_data['name'],
                                       description=form.cleaned_data['description'],
                                       university=in_university)
            new_course.teacher = current_teacher
            new_course.save()
            in_university.course_set.add(new_course)
            context = {
                'course': new_course,
            }
            return render(request, 'course2.html', context)

        context = {
            "form": form,
            "page_name" : "Add Course",
            "button_value" : "Add Course",
            "links" : ["login"],
        }
        return render(request, 'addCourse.html', context)

    return render(request, 'autherror.html')

def removeCourse2(request):
    if request.user.is_authenticated():
        current_teacher = Teacher.objects.get(teacher=request.user)
        in_university = current_teacher.university
        in_course_tag = request.GET.get('name', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.delete()

        teacher = Teacher.objects.get(teacher=request.user)
        teacher_course_list = teacher.course_set.all()
        context = {
            'courseList': teacher_course_list
        }
        return render(request, 'mycourses.html', context)

    # render error page if user is not logged in
    return render(request, 'autherror.html')

def addMem(request):
    if request.user.is_authenticated:
        current_teacher = Teacher.objects.get(teacher=request.user)
        in_university = current_teacher.university
        in_course_tag = request.GET.get('name', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)

        form = forms.addMemForm(request.POST or None)
        if form.is_valid():
            email1 = form.cleaned_data['email']
            #TODO: Make sure email entered belongs to Student and not just MyUser
            usernames = MyUser.objects.filter(email=email1)
            if len(usernames) == 0:
                context = {
                    "form": form,
                    "page_name": "Enroll a Student",
                    "button_value": "Enroll in Course",
                    "links": ["login"],
                    "course": in_course,
                }
                return render(request, 'addMem.html', context)
            username = usernames[0]
            in_course.members.add(username)
            in_course.save()
            username.course_set.add(in_course)
            username.save()

            teacher_course_list = current_teacher.course_set.all()
            context = {
                'courseList': teacher_course_list
            }
            return render(request, 'mycourses.html', context)
        context = {
            "form": form,
            "page_name": "Enroll a Student",
            "button_value": "Enroll in Course",
            "links": ["login"],
            "course": in_course,
        }

        return render(request, 'addMem.html', context)
    return render(request, 'autherror.html')

def removeMem(request):
    if request.user.is_authenticated():
        current_teacher = Teacher.objects.get(teacher=request.user)
        in_university = current_teacher.university
        in_course_tag = request.GET.get('name', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)

        email1= request.GET.get('email', 'None')
        usernames = MyUser.objects.filter(email=email1)
        username = usernames[0]

        in_course.members.remove(username)
        in_course.save()
        username.course_set.remove(in_course)
        username.save()

        context = {
            'course': in_course,
        }
        return render(request, 'course2.html', context)
    return render(request, 'autherror.html')
