"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms

class ProjectForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)
    skills = forms.CharField(label='Enter Skills (in CSV)', max_length=300)
