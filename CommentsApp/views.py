from django.shortcuts import render
from . import models
from . import forms
from GroupsApp.models import Group
from AuthenticationApp.models import Student
# Create your views here.
def getComments(request):
    comments_list = models.Comment.objects.all()
    context = {
        'comments' : comments_list,
    }
    return render(request, 'comments.html', context)
    
def getCommentForm(request):
    return render(request, 'commentForm.html')
def addComment(request):
    group = request.GET.get('group')
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            current_Group = Group.objects.get(name = group)

            new_comment = models.Comment(comment=form.cleaned_data['comment'])
            new_comment.owner = request.user
            new_comment.group = current_Group
            new_comment.save()
            comments_list = models.Comment.objects.filter(group=current_Group)
            members_list = current_Group.members.all()
            stud = []
            for member in members_list:
                stu = Student.objects.get(user=member)
                skills = stu.knownLanguages
                if skills not in stud:
                    stud.append(skills)
            context = {
                'group' : current_Group,
                'userIsMember': True,
                'comments' : comments_list,
                'student':stud,

            }
            return render(request, 'group.html', context)
        else:
            form = forms.CommentForm()
    return render(request, 'comments.html')