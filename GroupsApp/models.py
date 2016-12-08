"""GroupsApp Models

Created by Naman Patwari on 10/10/2016.
"""
from django.db import models

from ProjectsApp.models import Project
from AuthenticationApp.models import MyUser

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    members = models.ManyToManyField(MyUser)

    #Added project onetoone field for when the group is assigned to the project.
    project = models.OneToOneField(Project, related_name="assignedGroup", on_delete=models.SET_NULL, null=True)
    is_assignedToProject = models.BooleanField(default=False)

    def __str__(self):
        return self.name

