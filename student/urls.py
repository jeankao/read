# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from student.views import *
from student.views import GroupListView, ExamListView, TeamListView

urlpatterns = [
    # 選課
    url(r'^classroom/enroll/(?P<classroom_id>[^/]+)/$', login_required(views.classroom_enroll)),      
    url(r'^classroom/add/$', login_required(views.ClassroomAddListView.as_view())),  
    url(r'^classroom/(?P<role>\d+)/$', login_required(views.ClassroomListView.as_view())),
		url(r'^classroom/seat/(?P<enroll_id>\d+)/(?P<classroom_id>\d+)/$', login_required(views.seat_edit), name='seat_edit'),
    # 同學
    url(r'^classmate/(?P<classroom_id>\d+)/$', login_required(views.classmate)), 
    url(r'^loginlog/(?P<user_id>\d+)/$', login_required(views.LoginLogListView.as_view())),    
    #url(r'^calendar/(?P<classroom_id>\d+)/$', views.LoginCalendarClassView.as_view()),     	
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
    #公告
    url(r'^announce/(?P<classroom_id>\d+)/$', login_required(AnnounceListView.as_view()), name='announce-list'),
    #組別
    url(r'^group/(?P<classroom_id>\d+)/$', login_required(GroupListView.as_view()), name='group-list'),
    url(r'^group/list/(?P<group_id>\d+)/$', login_required(views.group_list), name='group-list'),
    url(r'^group/add/(?P<group_id>\d+)/(?P<number>\d+)/(?P<enroll_id>\d+)/$', login_required(views.group_join), name='group-join'),	
    url(r'^group/leader/(?P<group_id>\d+)/(?P<number>\d+)/(?P<enroll_id>\d+)/$', login_required(views.group_leader)),	
    #思辨
    url(r'^speculation/(?P<classroom_id>\d+)/(?P<bookmark>\d+)/$', login_required(SpeculationListView.as_view()), name='work-list'),  
    url(r'^speculation/submit/(?P<classroom_id>\d+)/(?P<index>\d+)/$', login_required(views.speculation_submit)),    
	url(r'^speculation/publish/(?P<classroom_id>\d+)/(?P<index>\d+)/(?P<action>\d+)/$', login_required(views.speculation_publish), name='speculation-publish'), 	
	url(r'^speculation/annotate/(?P<classroom_id>\d+)/(?P<index>\d+)/(?P<id>\d+)/$', login_required(SpeculationAnnotateView.as_view()), name='speculation-annotate'), 	
	url(r'^speculation/annotateclass/(?P<classroom_id>\d+)/(?P<index>\d+)/(?P<id>\d+)/$', login_required(SpeculationAnnotateClassView.as_view()), name='speculation-annotate-class'), 		
	url(r'^speculation/download/(?P<file_id>\d+)/$', views.speculation_download, name='forum-download'), 
	url(r'^speculation/showpic/(?P<file_id>\d+)/$', login_required(views.speculation_showpic), name='forum-showpic'), 		
    url(r'^speculation/score/$', login_required(views.speculation_score)), 
	#測驗
	url(r'^exam/(?P<classroom_id>\d+)/$', login_required(ExamListView.as_view())), 
	url(r'^exam/question/(?P<classroom_id>\d+)/(?P<exam_id>\d+)/(?P<examwork_id>\d+)/(?P<question_id>\d+)$', login_required(views.exam_question)), 	
	url(r'^exam/answer/$', login_required(views.exam_answer)), 	
	url(r'^exam/submit/(?P<classroom_id>\d+)/(?P<exam_id>\d+)/(?P<examwork_id>\d+)/$', login_required(views.exam_submit)), 
	url(r'^exam/score/(?P<classroom_id>\d+)/(?P<exam_id>\d+)/(?P<examwork_id>\d+)/(?P<user_id>\d+)/(?P<question_id>\d+)/$', login_required(views.exam_score)), 
    url(r'^video/log/$', views.video_log),
	#合作
	url(r'^team/(?P<classroom_id>\d+)/(?P<group_id>\d+)/$', login_required(TeamListView.as_view())), 
	#url(r'^team/stage/(?P<classroom_id>\d+)/(?P<grouping>\d+)/(?P<team_id>\d+)/$', login_required(views.team_stage)),                                 
    url(r'^team/content/(?P<classroom_id>\d+)/(?P<grouping>\d+)/(?P<team_id>\d+)/(?P<publish>\d+)/(?P<stage>\d+)/$', login_required(TeamContentListView.as_view())), 
    url(r'^team/stage/content/(?P<classroom_id>\d+)/(?P<grouping>\d+)/(?P<team_id>\d+)/(?P<publish>\d+)/(?P<stage>\d+)/$', login_required(TeamStageContentListView.as_view())), 
    url(r'^team/content/add/(?P<classroom_id>\d+)/(?P<grouping>\d+)/(?P<team_id>\d+)/$', login_required(TeamContentCreateView.as_view())),
    url(r'^team/content/delete/(?P<classroom_id>\d+)/(?P<grouping>\d+)/(?P<team_id>\d+)/(?P<content_id>\d+)/$', login_required(views.team_delete)),   
    url(r'^team/content/edit/(?P<classroom_id>\d+)/(?P<grouping>\d+)/(?P<team_id>\d+)/(?P<content_id>\d+)/$', login_required(views.team_edit)),    
    url(r'^team/publish/$', login_required(views.team_make_publish)),        
            	
    #課程
    url(r'^course/(?P<classroom_id>\d+)/$', login_required(CourseListView.as_view()), name='work-list'),  
    url(r'^course/content/(?P<classroom_id>\d+)/(?P<course_id>\d+)/$', login_required(CourseContentListView.as_view()), name='course-content'), 
    url(r'^course/content/progress/$', login_required(views.course_progress)),   
    url(r'^course/status/(?P<classroom_id>\d+)/(?P<course_id>\d+)/$', login_required(CourseStatusListView.as_view())),                                                
]