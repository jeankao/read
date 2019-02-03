# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from teacher.views import ClassroomListView, ClassroomCreateView
from teacher.views import GroupListView, GroupCreateView, GroupUpdateView
from teacher.views import ForumListView, ForumCreateView, ForumContentListView, ForumContentCreateView, ForumClassListView
from teacher.views import AssistantListView, ForumAllListView, ForumEditUpdateView, AnnounceCreateView
from teacher.views import SpeculationListView, SpeculationCreateView, SpeculationContentListView, SpeculationContentCreateView, SpeculationClassListView
from teacher.views import SpeculationAllListView, SpeculationEditUpdateView, SpeculationAnnotationListView, SpeculationAnnotationCreateView
from teacher.views import ExamListView, ExamCreateView, ExamEditUpdateView, ExamClassListView, ExamQuestionListView, ExamQuestionCreateView, ExamAllListView
from teacher.views import TeamListView, TeamCreateView, TeamEditUpdateView, TeamClassListView, VideoListView

urlpatterns = [
    url(r'^member/$', login_required(views.TeacherListView.as_view())),
    url(r'^student/(?P<teacher_id>\d+)/$', login_required(views.StudentListView.as_view())),  
    # 班級
    url(r'^classroom/$', login_required(views.ClassroomListView.as_view())),
    url(r'^classroom/add/$', login_required(views.ClassroomCreateView.as_view())),
    url(r'^classroom/edit/(?P<classroom_id>\d+)/$', login_required(views.classroom_edit)),
    url(r'^classroom/assistant/(?P<classroom_id>\d+)/$', login_required(views.classroom_assistant)),  
    url(r'^classroom/assistant/add/(?P<classroom_id>\d+)/$', login_required(views.AssistantListView.as_view())),  
    # 分組
    url(r'^group/(?P<classroom_id>\d+)/$', login_required(views.GroupListView.as_view())),
    url(r'^group/add/(?P<classroom_id>\d+)/$', login_required(views.GroupCreateView.as_view())),  
    url(r'^group/edit/(?P<classroom_id>\d+)/(?P<pk>\d+)/$', login_required(views.GroupUpdateView.as_view())),    
    url(r'^group/make/$', login_required(views.make)),   
    url(r'^group/make2/(?P<group_id>\d+)/(?P<action>\d+)/$', login_required(views.make2)),     
    #設定助教
    url(r'^assistant/$', login_required(views.AssistantClassroomListView.as_view())),  
    url(r'^assistant/make/$', login_required(views.assistant_make), name='make'),     
    # 退選
    url(r'^unenroll/(?P<enroll_id>\d+)/(?P<classroom_id>\d+)/$', login_required(views.unenroll)),  	
    # 討論區
    url(r'^forum/(?P<categroy>\d+)/(?P<categroy_id>\d+)/$', login_required(ForumAllListView.as_view()), name='forum-all'),  
    url(r'^forum/show/(?P<forum_id>\d+)/$', login_required(views.forum_show), name='forum-show'),    
    url(r'^forum/edit/(?P<classroom_id>\d+)/(?P<pk>\d+)/$', login_required(ForumEditUpdateView.as_view()), name='forum-edit'),   
    url(r'^forum/(?P<classroom_id>\d+)/$', login_required(ForumListView.as_view()), name='forum-list'),
    url(r'^forum/add/(?P<classroom_id>\d+)/$', login_required(ForumCreateView.as_view()), name='forum-add'),
    url(r'^forum/category/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.forum_categroy), name='forum-category'),  
    url(r'^forum/deadline/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.forum_deadline), name='forum-deadline'),  
    url(r'^forum/deadline/set/$', login_required(views.forum_deadline_set), name='forum-deatline-set'), 
    url(r'^forum/deadline/date/$', login_required(views.forum_deadline_date), name='forum-deatline-date'),   
    url(r'^forum/deadline/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.forum_deadline), name='forum-category'),   
    url(r'^forum/download/(?P<content_id>\d+)/$', views.forum_download, name='forum-download'),  
    url(r'^forum/content/(?P<forum_id>\d+)/$', login_required(ForumContentListView.as_view()), name='forum-content'), 
    url(r'^forum/content/add/(?P<forum_id>\d+)/$', login_required(ForumContentCreateView.as_view()), name='forum-content-add'),
    url(r'^forum/content/delete/(?P<forum_id>\d+)/(?P<content_id>\d+)/$', login_required(views.forum_delete), name='forum-content-delete'),   
    url(r'^forum/content/edit/(?P<forum_id>\d+)/(?P<content_id>\d+)/$', login_required(views.forum_edit), name='forum-content-edit'),    
    #url(r'^forum/class/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', views.forum_class, name='forum-class'),  
    url(r'^forum/class/(?P<forum_id>\d+)/$',  login_required(ForumClassListView.as_view()), name='forum-class'),    
    url(r'^forum/export/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.forum_export), name='forum-export'),   
    url(r'^forum/grade/(?P<classroom_id>\d+)/(?P<action>\d+)/$', login_required(views.forum_grade), name='forum-grade'),   
    #設定班級
    url(r'^forum/class/switch/$', login_required(views.forum_switch), name='make'),        
    #公告
    url(r'^announce/add/(?P<classroom_id>\d+)/$', login_required(AnnounceCreateView.as_view()), name='announce-add'),
    # 思辨區
    url(r'^speculation/(?P<categroy>\d+)/(?P<categroy_id>\d+)/$', login_required(SpeculationAllListView.as_view()), name='forum-all'),  
    url(r'^speculation/show/(?P<forum_id>\d+)/$', login_required(views.speculation_show), name='forum-show'),    
    url(r'^speculation/edit/(?P<classroom_id>\d+)/(?P<pk>\d+)/$', login_required(SpeculationEditUpdateView.as_view()), name='forum-edit'),   
    url(r'^speculation/(?P<classroom_id>\d+)/$', login_required(SpeculationListView.as_view()), name='forum-list'),
    url(r'^speculation/add/(?P<classroom_id>\d+)/$', login_required(SpeculationCreateView.as_view()), name='forum-add'),
    url(r'^speculation/category/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.speculation_categroy), name='forum-category'),  
    url(r'^speculation/deadline/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.speculation_deadline), name='forum-deadline'),  
    url(r'^speculation/deadline/set/$', login_required(views.speculation_deadline_set), name='forum-deatline-set'), 
    url(r'^speculation/deadline/date/$', login_required(views.speculation_deadline_date), name='forum-deatline-date'),   
    url(r'^speculation/deadline/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.speculation_deadline), name='forum-category'),   
    url(r'^speculation/download/(?P<content_id>\d+)/$', views.speculation_download, name='forum-download'),  
    url(r'^speculation/content/(?P<forum_id>\d+)/$', login_required(SpeculationContentListView.as_view()), name='forum-content'), 
    url(r'^speculation/content/add/(?P<forum_id>\d+)/$', login_required(SpeculationContentCreateView.as_view()), name='forum-content-add'),
    url(r'^speculation/content/delete/(?P<forum_id>\d+)/(?P<content_id>\d+)/$', login_required(views.speculation_delete), name='forum-content-delete'),   
    url(r'^speculation/content/edit/(?P<forum_id>\d+)/(?P<content_id>\d+)/$', login_required(views.speculation_edit), name='forum-content-edit'),    
    #url(r'^forum/class/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', views.forum_class, name='forum-class'),  
    url(r'^speculation/class/(?P<forum_id>\d+)/$',  login_required(SpeculationClassListView.as_view()), name='forum-class'),    
    url(r'^speculation/export/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.speculation_export), name='forum-export'),   
    url(r'^speculation/grade/(?P<classroom_id>\d+)/(?P<action>\d+)/$', login_required(views.speculation_grade)),   
    #設定班級
    url(r'^speculation/class/switch/$', login_required(views.speculation_switch), name='make'),
    #設定分組
    url(r'^speculation/group/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.speculation_group), name='group'),  
    url(r'^speculation/group/set/$', login_required(views.speculation_group_set), name='group'),   
    #文字註記
    url(r'^speculation/annotation/(?P<forum_id>\d+)/$', login_required(SpeculationAnnotationListView.as_view()), name='make'),   
    url(r'^speculation/annotation/add/(?P<forum_id>\d+)/$', login_required(SpeculationAnnotationCreateView.as_view()), name='forum-content-add'),
    url(r'^speculation/annotation/delete/(?P<forum_id>\d+)/(?P<content_id>\d+)/$', login_required(views.speculation_annotation_delete), name='forum-content-delete'),   
    url(r'^speculation/annotation/edit/(?P<forum_id>\d+)/(?P<content_id>\d+)/$', login_required(views.speculation_annotation_edit), name='forum-content-edit'),    
    #  測驗區
    url(r'^exam/(?P<categroy>\d+)/(?P<categroy_id>\d+)/$', login_required(ExamAllListView.as_view())),  
    url(r'^exam/(?P<classroom_id>\d+)/$', login_required(ExamListView.as_view())),
    url(r'^exam/add/(?P<classroom_id>\d+)/$', login_required(ExamCreateView.as_view())),
    url(r'^exam/edit/(?P<classroom_id>\d+)/(?P<pk>\d+)/$', login_required(ExamEditUpdateView.as_view())),   
    url(r'^exam/category/(?P<classroom_id>\d+)/(?P<exam_id>\d+)/$', login_required(views.exam_categroy)),  
    url(r'^exam/class/(?P<exam_id>\d+)/$',  login_required(ExamClassListView.as_view())), 
    url(r'^exam/class/switch/$', login_required(views.exam_switch)),        
    url(r'^exam/deadline/(?P<classroom_id>\d+)/(?P<exam_id>\d+)/$', login_required(views.exam_deadline)),  
    url(r'^exam/deadline/set/$', login_required(views.exam_deadline_set)), 
	    url(r'^exam/deadline/date/$', login_required(views.exam_deadline_date)),   
    url(r'^exam/round/(?P<classroom_id>\d+)/(?P<exam_id>\d+)$', login_required(views.exam_round)),   	
    url(r'^exam/round/set/$', login_required(views.exam_round_set)), 	
    url(r'^exam/question/(?P<exam_id>\d+)/$', login_required(ExamQuestionListView.as_view())), 
    url(r'^exam/question/add/(?P<exam_id>\d+)/$', login_required(ExamQuestionCreateView.as_view())),
    url(r'^exam/question/delete/(?P<exam_id>\d+)/(?P<question_id>\d+)/$', login_required(views.exam_question_delete)),   
    url(r'^exam/question/edit/(?P<exam_id>\d+)/(?P<question_id>\d+)/$', login_required(views.exam_question_edit)), 
    url(r'^exam/score/(?P<classroom_id>\d+)/(?P<exam_id>\d+)/$', login_required(views.exam_score)), 	
	  #大量匯入選擇題
    url(r'^exam/import2/upload/(?P<exam_id>\d+)/$', login_required(views.exam_import_sheet)),   	
    url(r'^exam/import2/question/(?P<exam_id>\d+)/$', login_required(views.exam_import_question)),   
    # 合作區
    #url(r'^team/(?P<categroy>\d+)/(?P<categroy_id>\d+)/$', login_required(TeamAllListView.as_view())),  
    #url(r'^forum/show/(?P<forum_id>\d+)/$', login_required(views.forum_show), name='forum-show'),    
    url(r'^team/edit/(?P<classroom_id>\d+)/(?P<pk>\d+)/$', login_required(TeamEditUpdateView.as_view())),   
    url(r'^team/(?P<classroom_id>\d+)/$', login_required(TeamListView.as_view())),
    url(r'^team/add/(?P<classroom_id>\d+)/$', login_required(TeamCreateView.as_view())),
    url(r'^team/category/(?P<classroom_id>\d+)/(?P<team_id>\d+)/$', login_required(views.team_categroy)),  
    url(r'^team/deadline/(?P<classroom_id>\d+)/(?P<team_id>\d+)/$', login_required(views.team_deadline)),  
    url(r'^team/deadline/set/$', login_required(views.team_deadline_set)), 
    url(r'^team/deadline/date/$', login_required(views.team_deadline_date)),   
    url(r'^team/deadline/(?P<classroom_id>\d+)/(?P<team_id>\d+)/$', login_required(views.team_deadline)),   
    #url(r'^forum/download/(?P<content_id>\d+)/$', views.forum_download, name='forum-download'),  
    #url(r'^forum/content/(?P<forum_id>\d+)/$', login_required(ForumContentListView.as_view()), name='forum-content'), 
    #url(r'^forum/content/add/(?P<forum_id>\d+)/$', login_required(ForumContentCreateView.as_view()), name='forum-content-add'),
    #url(r'^forum/content/delete/(?P<forum_id>\d+)/(?P<content_id>\d+)/$', login_required(views.forum_delete), name='forum-content-delete'),   
    #url(r'^forum/content/edit/(?P<forum_id>\d+)/(?P<content_id>\d+)/$', login_required(views.forum_edit), name='forum-content-edit'),    
    url(r'^team/class/(?P<classroom_id>\d+)/(?P<team_id>\d+)/$', views.team_class),  
    url(r'^team/class/(?P<team_id>\d+)/$',login_required(TeamClassListView.as_view())),  	
    url(r'^team/class/switch/$', login_required(views.team_switch)),      	
    url(r'^team/group/(?P<classroom_id>\d+)/(?P<team_id>\d+)/$', login_required(views.team_group)),
    url(r'^team/group/set/$', login_required(views.team_group_set)),	
	  # 影片觀看記錄
    url(r'^video/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/(?P<work_id>\d+)/$', views.EventVideoView.as_view()),
    url(r'^video/length/$', views.video_length),	
		url(r'^video/user/(?P<classroom_id>\d+)/(?P<content_id>\d+)/(?P<user_id>\d+)/$', VideoListView.as_view()), 	
]