"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms
from ProjectsApp.models import Project
class GroupForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)


class addMemForm(forms.Form):
    email = forms.CharField(label='Email',max_length=50)

class assignProjForm(forms.Form):
    project = forms.ModelChoiceField(label="Projects Available",
                                     queryset=Project.objects.filter(is_assignedToGroup=False), required=True)

