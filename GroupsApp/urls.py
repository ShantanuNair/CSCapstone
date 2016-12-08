"""GroupsApp URL

Created by Naman Patwari on 10/10/2016.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^group/all$', views.getGroups, name='Groups'),
	url(r'^group/form$', views.getGroupForm, name='GroupForm'),
    url(r'^group/formsuccess$', views.getGroupFormSuccess, name='GroupFormSuccess'),
    url(r'^group/join$', views.joinGroup, name='GJoin'),
    url(r'^group/unjoin$', views.unjoinGroup, name='GUnjoin'),
    url(r'^group/mygroups$', views.getMyGroups, name='GMine'),
    url(r'^group$', views.getGroup, name='Group'),
    url(r'^group/addmem$', views.addMem, name='GAddMem'),
    url(r'^group/assignproj$', views.assignProj, name='GAssignProj'),
    url(r'^group/suggestproj$', views.suggestProj, name='GSuggestProj'),
    url(r'^group/leaveproj$', views.leaveProj, name='GLeaveProj'),

]