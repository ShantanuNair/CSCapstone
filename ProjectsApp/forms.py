"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms

class ProjectForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)
    skills = forms.CharField(label='skills', max_length=300)
    experience = forms.CharField(label='experience', max_length=300)
    specialty = forms.CharField(label='specialty', max_length=50)
