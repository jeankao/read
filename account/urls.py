# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # post views
    url(r'^dashboard/(?P<action>\d+)/$',  views.MessageListView.as_view(), name='dashboard'),    
    #登入
    url(r'^login/$', views.user_login, name='login'),
    #登出
    url(r'^logout/$',auth_views.logout),
    url(r'^suss_logout/(?P<user_id>\d+)/$', views.suss_logout),    
    #列出所有帳號
    url(r'^userlist/$', login_required(views.UserListView.as_view())),      
    #管理介面 
    url(r'^admin/$', login_required(views.admin)),        
    url(r'^admin/domain/$', login_required(views.DomainListView.as_view())),     
    url(r'^admin/domain/add/$', login_required(views.DomainCreateView.as_view())),     
    url(r'^admin/domain/edit/(?P<pk>\d+)/$', login_required(views.DomainUpdateView.as_view())),
    url(r'^admin/sitename/(?P<pk>\d+)/$', login_required(views.SitenameUpdateView.as_view())), 
    url(r'^admin/siteimage/$', login_required(views.siteimage)),     
    url(r'^admin/level/$', login_required(views.LevelListView.as_view())),     
    url(r'^admin/level/add/$', login_required(views.LevelCreateView.as_view())),     
    url(r'^admin/level/edit/(?P<pk>\d+)/$', login_required(views.LevelUpdateView.as_view())),  
    #註冊帳號
    url(r'^register/$', views.register, name='register'),   
    #個人檔案
    url(r'^profile/(?P<user_id>\d+)/$', login_required(views.profile)),    
    #修改密碼
    url(r'^password-change/$', login_required(auth_views.password_change), name='password_change'),
    url(r'^password-change/done/$', login_required(auth_views.password_change_done), name='password_change_done'),    
    url(r'^password/(?P<user_id>\d+)/$', login_required(views.password)),
    #修改真實姓名
    url(r'^realname/(?P<user_id>\d+)/$', login_required(views.adminrealname)),    
    url(r'^realname/$', login_required(views.realname), name='realname'), 
    #修改學校
    url(r'^school/$', login_required(views.adminschool)),     
    #修改信箱
    url(r'^email/$', login_required(views.adminemail)),    
    #積分記錄
    url(r'^log/(?P<kind>\d+)/(?P<user_id>\d+)/$', login_required(views.LogListView.as_view())),	    
    #設定教師
    url(r'^teacher/make/$', login_required(views.make), name='make'),    
    # 列所出有圖像
    url(r'^avatar/$', login_required(views.avatar)),  
    # 讀取訊息
    url(r'^message/(?P<messagepoll_id>\d+)/$', login_required(views.message)),
    # 私訊
    url(r'^line/$', login_required(views.LineListView.as_view())),    
    url(r'^line/class/(?P<classroom_id>\d+)/$', login_required(views.LineClassListView.as_view())),        
    url(r'^line/add/(?P<classroom_id>\d+)/(?P<user_id>\d+)/$', login_required(views.LineCreateView.as_view())),
    url(r'^line/detail/(?P<classroom_id>\d+)/(?P<message_id>\d+)/$', login_required(views.line_detail)),
	  url(r'^line/download/(?P<file_id>\d+)/$', views.line_download, name='forum-download'), 
	  url(r'^line/showpic/(?P<file_id>\d+)/$', login_required(views.line_showpic), name='forum-showpic'), 	
  
    #訪客
    url(r'^visitor/$', views.VisitorListView.as_view()),    
    url(r'^visitorlog/(?P<visitor_id>\d+)/$', login_required(views.VisitorLogListView.as_view())),             
    

    #系統事件記錄
    url(r'^event/(?P<user_id>\d+)/$', login_required(views.EventListView.as_view())),
    url(r'^event/admin/$', login_required(views.EventAdminListView.as_view())),
    url(r'^event/admin/classroom/(?P<classroom_id>\d+)/$', login_required(views.EventAdminClassroomListView.as_view())),
    url(r'^event/calendar/(?P<user_id>\d+)/$', login_required(views.EventCalendarView.as_view())),	  
    url(r'^event/timeline/(?P<user_id>\d+)/$', login_required(views.EventTimeLineView.as_view())), 
    url(r'^event/timelog/(?P<user_id>\d+)/(?P<hour>\d+)/$', login_required(views.EventTimeLogView.as_view())),   
    url(r'^event/video/(?P<classroom_id>\d+)/$', login_required(views.EventVideoView.as_view())),   
    #討論區作業
    url(r'^forum/(?P<user_id>\d+)/$', login_required(views.ForumListView.as_view())),	 
    #設定家長
    url(r'^parent/$', login_required(views.ParentListView.as_view())),
    url(r'^parent/search/$', login_required(views.ParentSearchListView.as_view())),
    url(r'^parent/child/$', login_required(views.ParentChildListView.as_view())),  
    url(r'^parent/make/$', login_required(views.parent_make), name='parent_make'),      
]