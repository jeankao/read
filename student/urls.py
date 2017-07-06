# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from student.views import WorkListView, ForumListView

urlpatterns = [
    # 選課
    url(r'^classroom/enroll/(?P<classroom_id>[^/]+)/$', login_required(views.classroom_enroll)),      
    url(r'^classroom/add/$', login_required(views.classroom_add)),  
    url(r'^classroom/$', login_required(views.ClassroomListView.as_view())),
		url(r'^classroom/seat/(?P<enroll_id>\d+)/(?P<classroom_id>\d+)/$', login_required(views.seat_edit), name='seat_edit'),
    # 同學
    url(r'^classmate/(?P<classroom_id>\d+)/$', login_required(views.classmate)), 
    url(r'^loginlog/(?P<user_id>\d+)/$', login_required(views.LoginLogListView.as_view())),    
    #url(r'^calendar/(?P<classroom_id>\d+)/$', views.LoginCalendarClassView.as_view()),     	
    #作業
    url(r'^work/(?P<classroom_id>\d+)/$', login_required(WorkListView.as_view()), name='work-list'),  
    url(r'^work/submit/(?P<classroom_id>\d+)/(?P<index>\d+)/$', login_required(views.submit)),    
    url(r'^work/show/(?P<index>\d+)/$', login_required(views.show)),      
    url(r'^work/video/(?P<classroom_id>\d+)/(?P<index>\d+)/$', login_required(views.video)), 	
    url(r'^work/memo/(?P<classroom_id>\d+)/(?P<index>\d+)/$', login_required(views.memo)), 
	  url(r'^work/rank/(?P<index>\d+)/$', login_required(views.rank)), 	
    #作業
    url(r'^forum/(?P<classroom_id>\d+)/(?P<bookmark>\d+)/$', login_required(ForumListView.as_view()), name='work-list'),  
    url(r'^forum/submit/(?P<classroom_id>\d+)/(?P<index>\d+)/$', login_required(views.forum_submit)),    
    url(r'^forum/file_delete/$', login_required(views.forum_file_delete)), 	
    url(r'^forum/memo/(?P<classroom_id>\d+)/(?P<index>\d+)/(?P<action>\d+)/$', login_required(views.forum_memo)),  
    url(r'^forum/show/(?P<index>\d+)/(?P<user_id>\d+)/(?P<classroom_id>\d+)/$', login_required(views.forum_show)), 	
    url(r'^forum/history/(?P<user_id>\d+)/(?P<index>\d+)/(?P<classroom_id>\d+)/$', login_required(views.forum_history)),  
    url(r'^forum/like/$', login_required(views.forum_like), name='like'),    
    url(r'^forum/reply/$', login_required(views.forum_reply), name='reply'),    	
    url(r'^forum/people/$', login_required(views.forum_people), name='people'), 
    url(r'^forum/guestbook/$', login_required(views.forum_guestbook), name='guestbook'), 	
    url(r'^forum/score/$', login_required(views.forum_score), name='score'),   
    url(r'^forum/jieba/(?P<classroom_id>\d+)/(?P<index>\d+)/$', login_required(views.forum_jieba)), 	
    url(r'^forum/word/(?P<classroom_id>\d+)/(?P<index>\d+)/(?P<word>[^/]+)/$', login_required(views.forum_word)),  
	  url(r'^forum/download/(?P<file_id>\d+)/$', views.forum_download, name='forum-download'), 
	  url(r'^forum/showpic/(?P<file_id>\d+)/$', login_required(views.forum_showpic), name='forum-showpic'), 	
	  url(r'^forum/publish/(?P<classroom_id>\d+)/(?P<index>\d+)/(?P<action>\d+)/$', login_required(views.forum_publish), name='forum-publish'), 	
]