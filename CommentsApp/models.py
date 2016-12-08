from django.db import models

from GroupsApp.models import Group
from ProjectsApp.models import Project
from AuthenticationApp.models import MyUser# Create your models here.

class Comment(models.Model):
    time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=500)
    group = models.ForeignKey(Group,related_name="comments_group", on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)

    def __str__(self):
        # toString() method
        return str(self.time) + ", " + self.comment