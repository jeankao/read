# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from student.views import WorkListView, ForumListView

urlpatterns = [
    # 選課
    url(r'^classroom/enroll/(?P<classroom_id>[^/]+)/$', views.classroom_enroll),      
    url(r'^classroom/add/$', views.classroom_add),  
    url(r'^classroom/$', views.ClassroomListView.as_view()),
		url(r'^classroom/seat/(?P<enroll_id>\d+)/(?P<classroom_id>\d+)/$', views.seat_edit, name='seat_edit'),
    # 同學
    url(r'^classmate/(?P<classroom_id>\d+)/$', views.classmate), 
    url(r'^loginlog/(?P<user_id>\d+)/$', views.LoginLogListView.as_view()),    
    #url(r'^calendar/(?P<classroom_id>\d+)/$', views.LoginCalendarClassView.as_view()),     	
    #作業
    url(r'^work/(?P<classroom_id>\d+)/$', login_required(WorkListView.as_view()), name='work-list'),  
    url(r'^work/submit/(?P<index>\d+)/$', views.submit),    
    url(r'^work/show/(?P<index>\d+)/$', views.show),      
    url(r'^work/video/(?P<classroom_id>\d+)/(?P<index>\d+)/$', views.video), 	
    url(r'^work/memo/(?P<classroom_id>\d+)/(?P<index>\d+)/$', views.memo), 
	  url(r'^work/rank/(?P<index>\d+)/$', views.rank), 	
    #作業
    url(r'^forum/(?P<classroom_id>\d+)/$', login_required(ForumListView.as_view()), name='work-list'),  
    url(r'^forum/submit/(?P<index>\d+)/$', views.forum_submit),    
    url(r'^forum/show/(?P<index>\d+)/$', views.forum_show),  
    url(r'^forum/memo/(?P<classroom_id>\d+)/(?P<index>\d+)/$', views.forum_memo),  
    url(r'^forum/history/(?P<user_id>\d+)/(?P<index>\d+)/$', views.forum_history),  
    url(r'^forum/like/$', views.forum_like, name='like'),    
    url(r'^forum/people/$', views.forum_people, name='like'), 
    url(r'^forum/score/$', views.forum_score, name='score'),    
]