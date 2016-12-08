"""AuthenticationApp URL Configuration

Created by Naman Patwari on 10/4/2016.
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.auth_login, name='Login'),
    url(r'^logout$', views.auth_logout, name='Logout'),
    url(r'^register$', views.auth_register, name='Register'),
    url(r'^update$', views.update_profile, name='UpdateProfile'),
    url(r'^profile$', views.view_profile, name='ViewProfile'),
    url(r'^studentProfile$', views.view_studentProfile, name='ViewStudentProfile'),
    url(r'^bookmarks$', views.view_bookmarks, name='ViewBookmarks'),
    url(r'^bookmarks/add$', views.add_bookmark, name='AddBookmark'),
    url(r'^bookmarks/remove$', views.remove_bookmark, name='RemoveBookmark'),
]