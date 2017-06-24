# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from teacher.views import ClassroomListView, ClassroomCreateView, WorkListView, WorkCreateView, ForumListView, ForumCreateView, ForumContentListView, ForumContentCreateView

urlpatterns = [
    # 班級
    url(r'^classroom/$', login_required(views.ClassroomListView.as_view()), name='classroom-list'),
    url(r'^classroom/add/$', login_required(views.ClassroomCreateView.as_view()), name='classroom-add'),
    url(r'^classroom/edit/(?P<classroom_id>\d+)/$', views.classroom_edit, name='classroom-edit'),
    # 退選
    url(r'^unenroll/(?P<enroll_id>\d+)/(?P<classroom_id>\d+)/$', views.unenroll),  	
    # 搜查線
    url(r'^work/(?P<classroom_id>\d+)/$', login_required(WorkListView.as_view()), name='work-list'),
    url(r'^work/add/(?P<classroom_id>\d+)/$', login_required(WorkCreateView.as_view()), name='work-add'),
    url(r'^work/edit/(?P<classroom_id>\d+)/$', views.work_edit, name='work-edit'),  
    url(r'^work/class/(?P<classroom_id>\d+)/(?P<work_id>\d+)/$', views.work_class, name='work-class'),  
    # 討論區
    url(r'^forum/(?P<classroom_id>\d+)/$', login_required(ForumListView.as_view()), name='forum-list'),
    url(r'^forum/add/(?P<classroom_id>\d+)/$', login_required(ForumCreateView.as_view()), name='forum-add'),
    url(r'^forum/download/(?P<content_id>\d+)/$', views.forum_download, name='forum-add'),  
    url(r'^forum/content/(?P<forum_id>\d+)/$', login_required(ForumContentListView.as_view()), name='forum-content'), 
    url(r'^forum/content/add/(?P<forum_id>\d+)/$', login_required(ForumContentCreateView.as_view()), name='forum-content-add'),
    url(r'^forum/content/delete/(?P<forum_id>\d+)/(?P<content_id>\d+)/$', views.forum_delete, name='forum-content-delete'),   
    url(r'^forum/class/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', views.forum_class, name='forum-class'),  
]