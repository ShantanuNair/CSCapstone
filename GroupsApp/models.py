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

    #Added project foreign key for when the group is assigned to the project.
    project = models.ForeignKey(Project, related_name="project", null=True)

    def __str__(self):
        return self.name