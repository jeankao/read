# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, CreateView
from student.models import Enroll, EnrollGroup, SWork, SFWork, SFReply, SFContent, SSpeculationWork, SSpeculationContent
from teacher.models import Classroom, TWork, FWork, FContent, FClass, Assistant, SpeculationClass, SpeculationWork, SpeculationContent, SpeculationAnnotation
from account.models import VisitorLog,  Profile, Parent, Log, Message
from student.forms import EnrollForm, SeatForm, SubmitForm, ForumSubmitForm, SpeculationSubmitForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
import re
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
import jieba
from uuid import uuid4
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.db.models import F
from account.avatar import *
from django.db.models import Q

def is_event_open(request):
		return True


def is_classmate(student_id, user_id):
    enrolls = Enroll.objects.filter(student_id=student_id)
    for enroll in enrolls:
        classroom = Classroom.objects.get(id=enroll.classroom_id)
        enrolls2 = Enroll.objects.filter(classroom_id=classroom.id)
        for enroll2 in enrolls2:
            if user_id == enroll2.student_id:
                return True
    return False
	
def in_classroom(classroom_id, user_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    for enroll in enrolls:
        if user_id == enroll.student_id:
            return True
    return False	
	
def is_parent(student_id, user_id):
    parents = Parent.objects.filter(parent_id=user_id, student_id=student_id)
    if len(parents)> 0:
        return True
    return False
	
def is_teacher(classroom_id, user_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if user_id == classroom.teacher_id:
        return True
    return False
	
def is_assistant(classroom_id, user_id):
    assistants = Assistant.objects.filter(classroom_id=classroom_id, user_id=user_id)
    if len(assistants)>0 :
        return True
    return False	
   
# 列出選修的班級
class ClassroomListView(ListView):
    model = Enroll
    context_object_name = 'enrolls'
    paginate_by = 30
    template_name = 'student/classroom.html'
    
    def get_queryset(self):
        queryset = []
        enrolls = Enroll.objects.filter(student_id=self.request.user.id).order_by("-id")
        for enroll in enrolls :
          classroom = Classroom.objects.get(id=enroll.classroom_id)
          queryset.append([enroll, classroom.teacher_id])
        return queryset         			
    
# 查看可加入的班級
class ClassroomAddListView(ListView):
    context_object_name = 'classroom_teachers'
    paginate_by = 20
    template_name = 'student/classroom_add.html'
    
    def get_queryset(self):
        # 記錄系統事件
        if is_event_open(self.request) :           
            log = Log(user_id=self.request.user.id, event='查看加入班級')
            log.save()         
        if self.request.GET.get('classroom') != None:
            keyword = self.request.GET.get('classroom')
            teacher_ids = []
            teachers = User.objects.filter(first_name__icontains=keyword)
            for teacher in teachers:
                teacher_ids.append(teacher.id)
            classrooms = Classroom.objects.filter(Q(name__icontains=keyword) | Q(teacher_id__in=teacher_ids)).order_by('-id')
        else :
            classrooms = Classroom.objects.all().order_by('-id')
        classroom_teachers = []						
        for classroom in classrooms:
            enroll = Enroll.objects.filter(student_id=self.request.user.id, classroom_id=classroom.id)
            if enroll.exists():
                classroom_teachers.append([classroom,classroom.teacher.first_name,1])
            else:
                classroom_teachers.append([classroom,classroom.teacher.first_name,0]) 
        return classroom_teachers

    def get_context_data(self, **kwargs):
        context = super(ClassroomAddListView, self).get_context_data(**kwargs)
        classroom = self.request.GET.get('classroom')
        context.update({'classroom': classroom})
        return context	
			
def classroom_add(request):
        if self.request.GET.get('classroom') != None:
            keyword = self.request.GET.get('classroom')
            classrooms = Classroom.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword)).order_by('-id')
            classrooms = Classroom.objects.all().order_by('-id')
        else :
            queryset = User.objects.all().order_by('-id')					
        classroom_teachers = []
        for classroom in classrooms:
            enroll = Enroll.objects.filter(student_id=request.user.id, classroom_id=classroom.id)
            if enroll.exists():
                classroom_teachers.append([classroom,classroom.teacher.first_name,1])
            else:
                classroom_teachers.append([classroom,classroom.teacher.first_name,0])   
        return render_to_response('student/classroom_add.html', {'classroom_teachers':classroom_teachers}, context_instance=RequestContext(request))
    
# 加入班級
def classroom_enroll(request, classroom_id):
        scores = []
        if request.method == 'POST':
                form = EnrollForm(request.POST)
                if form.is_valid():
                    try:
                        classroom = Classroom.objects.get(id=classroom_id)
                        if classroom.password == form.cleaned_data['password']:
                                enroll = Enroll(classroom_id=classroom_id, student_id=request.user.id, seat=form.cleaned_data['seat'])
                                enroll.save()                                
                        else:
                                return render_to_response('message.html', {'message':"選課密碼錯誤"}, context_instance=RequestContext(request))
                      
                    except Classroom.DoesNotExist:
                        pass
                    
                    
                    return redirect("/student/classroom/")
        else:
            form = EnrollForm()
        return render_to_response('student/classroom_enroll.html', {'form':form}, context_instance=RequestContext(request))
        
# 修改座號
def seat_edit(request, enroll_id, classroom_id):
    enroll = Enroll.objects.get(id=enroll_id)
    if request.method == 'POST':
        form = SeatForm(request.POST)
        if form.is_valid():
            enroll.seat =form.cleaned_data['seat']
            enroll.save()
            classroom_name = Classroom.objects.get(id=classroom_id).name
            return redirect('/student/classroom')
    else:
        form = SeatForm(instance=enroll)

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))  



# 查看班級學生
def classmate(request, classroom_id):
        enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
        enroll_ids = []
        for enroll in enrolls:
            enroll_ids.append(enroll.student_id)
        enroll_group = []
        classroom=Classroom.objects.get(id=classroom_id)
        parent_pool = Parent.objects.filter(student_id__in=enroll_ids)
        for enroll in enrolls:
            login_times = len(VisitorLog.objects.filter(user_id=enroll.student_id))
            parents = filter(lambda w: w.student_id==enroll.student_id, parent_pool)
            enroll_group.append([enroll, login_times, parents])	
        return render_to_response('student/classmate.html', {'classroom':classroom, 'enrolls':enroll_group}, context_instance=RequestContext(request))

# 登入記錄
class LoginLogListView(ListView):
    context_object_name = 'visitorlogs'
    paginate_by = 20
    template_name = 'student/login_log.html'
    def get_queryset(self):
        visitorlogs = VisitorLog.objects.filter(user_id=self.kwargs['user_id']).order_by("-id")         
        return visitorlogs
        
    def get_context_data(self, **kwargs):
        context = super(LoginLogListView, self).get_context_data(**kwargs)
        if self.request.GET.get('page') :
            context['page'] = int(self.request.GET.get('page')) * 20 - 20
        else :
            context['page'] = 0
        return context        
        
      
# 列出所有作業
class WorkListView(ListView):
    model = TWork
    context_object_name = 'works'
    template_name = 'student/work_list.html'    
    paginate_by = 20
    
    def get_queryset(self):
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
       
        queryset = TWork.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(WorkListView, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        return context	    

    # 限本班同學
    def render_to_response(self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(WorkListView, self).render_to_response(context)    
			
def submit(request, index):
        scores = []
        works = SWork.objects.filter(index=index, student_id=request.user.id)		
        if request.method == 'POST':
            form = SubmitForm(request.POST, request.FILES)
            if form.is_valid():						
                try: 
                    work = SWork.objects.get(index=index, student_id=request.user.id)
                except ObjectDoesNotExist:
                    work = SWork(index=index, student_id=request.user.id)		
                work.youtube=form.cleaned_data['youtube']
                work.memo=form.cleaned_data['memo']
                work.save()

                return redirect("/student/work/show/"+index)
            else:
                return render_to_response('form.html', {'error':form.errors}, context_instance=RequestContext(request))
        else:
            if not works.exists():
                form = SubmitForm()
            else:
                form = SubmitForm(instance=works[0])
        return render_to_response('form.html', {'form':form, 'scores':scores, 'index':index}, context_instance=RequestContext(request))

def show(request, index):
    work = []
    try:
        work = SWork.objects.get(index=index, student_id=request.user.id)
    except ObjectDoesNotExist:
        pass    
    return render_to_response('student/work_show.html', {'work':work}, context_instance=RequestContext(request))

    
def rank(request, index):
    works = SWork.objects.filter(index=index).order_by("id")
    return render_to_response('student/work_rank.html', {'works':works}, context_instance=RequestContext(request))

# 查詢某作業所有同學心得
def memo(request, classroom_id, index):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    datas = []
    for enroll in enrolls:
        try:
            work = SWork.objects.get(index=index, student_id=enroll.student_id)
            datas.append([enroll.seat, enroll.student.first_name, work.memo])
        except ObjectDoesNotExist:
            datas.append([enroll.seat, enroll.student.first_name, ""])
    def getKey(custom):
        return custom[0]
    datas = sorted(datas, key=getKey)	
  
    return render_to_response('student/work_memo.html', {'datas': datas}, context_instance=RequestContext(request))
	
# 查詢某作業所有同學影片和心得
def video(request, classroom_id, index):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    datas = []
    for enroll in enrolls:
        try:
            work = SWork.objects.get(index=index, student_id=enroll.student_id)
            datas.append([enroll.seat, enroll.student.first_name, work.memo, work.youtube])
        except ObjectDoesNotExist:
            datas.append([enroll.seat, enroll.student.first_name, "", ""])
    def getKey(custom):
        return custom[0]
    datas = sorted(datas, key=getKey)	
  
    return render_to_response('student/work_video.html', {'datas': datas}, context_instance=RequestContext(request))
	
# 列出所有討論主題
class ForumListView(ListView):
    model = SFWork
    context_object_name = 'works'
    template_name = 'student/forum_list.html'    
    
    def get_queryset(self):
        queryset = []
        fclass_dict = dict(((fclass.forum_id, fclass) for fclass in FClass.objects.filter(classroom_id=self.kwargs['classroom_id'])))	
        #fclasses = FClass.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")
        fworks = FWork.objects.filter(id__in=fclass_dict.keys()).order_by("-id")
        sfwork_pool = SFWork.objects.filter(student_id=self.request.user.id).order_by("-id")
        for fwork in fworks:
            sfworks = filter(lambda w: w.index==fwork.id, sfwork_pool)
            if len(sfworks)> 0 :
                queryset.append([fwork, sfworks[0].publish, fclass_dict[fwork.id], len(sfworks)])
            else :
                queryset.append([fwork, False, fclass_dict[fwork.id], 0])
        def getKey(custom):
            return custom[2].publication_date, custom[2].forum_id
        queryset = sorted(queryset, key=getKey, reverse=True)	
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(ForumListView, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        context['bookmark'] =  self.kwargs['bookmark']
        context['fclasses'] = dict(((fclass.forum_id, fclass) for fclass in FClass.objects.filter(classroom_id=self.kwargs['classroom_id'])))
        return context	    

    # 限本班同學
    def render_to_response(self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(ForumListView, self).render_to_response(context)    

# 發表心得
def forum_publish(request, classroom_id, index, action):
    if action == "1":
        try:
            works = SFWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
            work = works[0]
            work.publish = True
            work.save()
        except ObjectDoesNotExist:
            pass
        return redirect("/student/forum/memo/"+classroom_id+"/"+index+"/0")
    elif action == "0":
        return redirect("/student/forum/memo/"+classroom_id+"/"+index+"/0")
    else :
        return render_to_response('student/forum_publish.html', {'classroom_id': classroom_id, 'index': index}, context_instance=RequestContext(request))
	

def forum_submit(request, classroom_id, index):
        scores = []
        works = SFWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
        contents = FContent.objects.filter(forum_id=index)
        fwork = FWork.objects.get(id=index)
        if request.method == 'POST':
            form = ForumSubmitForm(request.POST, request.FILES)
            #第一次上傳加上積分
            works = SFWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
            publish = False
            if len(works)==0:
                update_avatar(request.user.id, 1, 2)
            else:
                publish = works[0].publish
            work = SFWork(index=index, student_id=request.user.id, publish=publish)
            work.save()
            if request.FILES:
                content = SFContent(index=index, student_id=request.user.id)
                myfile =  request.FILES.get("file", "")
                fs = FileSystemStorage()
                filename = uuid4().hex
                content.title = myfile.name
                content.work_id = work.id
                content.filename = str(request.user.id)+"/"+filename
                fs.save("static/upload/"+str(request.user.id)+"/"+filename, myfile)
                content.save()
            if form.is_valid():							
                work.memo=form.cleaned_data['memo']
                work.save()
                if not works:
                    return redirect("/student/forum/publish/"+classroom_id+"/"+index+"/2")	
                elif not works[0].publish:
                    return redirect("/student/forum/publish/"+classroom_id+"/"+index+"/2")
                return redirect("/student/forum/memo/"+classroom_id+"/"+index+"/0")
            else:
                return render_to_response('student/forum_form.html', {'error':form.errors}, context_instance=RequestContext(request))
        else:
            if not works.exists():
                work = SFWork(index=0, publish=False)
                form = ForumSubmitForm()
            else:
                work = works[0]
                form = ForumSubmitForm()
            files = SFContent.objects.filter(index=index, student_id=request.user.id,visible=True).order_by("-id")
            subject = FWork.objects.get(id=index).title
        return render_to_response('student/forum_form.html', {'classroom_id':classroom_id, 'subject':subject, 'files':files, 'index': index, 'fwork':fwork, 'works':works, 'work':work, 'form':form, 'scores':scores, 'index':index, 'contents':contents}, context_instance=RequestContext(request))

def forum_show(request, index, user_id, classroom_id):
		if not (is_classmate(int(user_id), request.user.id) or is_teacher(classroom_id, request.user.id) or is_parent(user_id,request.user.id)) :
			return redirect("/")	
		forum = FWork.objects.get(id=index)
		teacher_id = forum.teacher_id
		work = []
		replys = []
		files = []
		works = SFWork.objects.filter(index=index, student_id=user_id).order_by("-id")
		contents = FContent.objects.filter(forum_id=index).order_by("id")
		publish = False
		if len(works)>0:
			work_new = works[0]
			work_first = works.last()
			publish = work_first.publish
			replys = SFReply.objects.filter(index=index, work_id=work_first.id).order_by("-id")	
			files = SFContent.objects.filter(index=index, student_id=user_id, visible=True).order_by("-id")	
			return render_to_response('student/forum_show.html', {'publish':publish, 'classroom_id':classroom_id, 'contents':contents, 'replys':replys, 'files':files, 'forum':forum, 'user_id':user_id, 'work_first':work_first, 'work_new':work_new, 'teacher_id':teacher_id, 'works': works, 'is_teacher':is_teacher(classroom_id, request.user.id)}, context_instance=RequestContext(request))
		else :
			message = "尚無作品"
			return render_to_response('message.html', {'message':message}, context_instance=RequestContext(request))
		
 # 查詢某作業所有同學心得
def forum_memo(request, classroom_id, index, action):
	if not in_classroom(classroom_id, request.user.id):
		return redirect("/")
	enrolls = Enroll.objects.filter(classroom_id=classroom_id)
	datas = []
	contents = FContent.objects.filter(forum_id=index).order_by("-id")
	fwork = FWork.objects.get(id=index)
	teacher_id = fwork.teacher_id
	subject = fwork.title
	if action == "2":
		works_pool = SFWork.objects.filter(index=index, score=5).order_by("-id")
	else:
	  # 一次取得所有 SFWork	
	  works_pool = SFWork.objects.filter(index=index).order_by("-id", "publish")
	reply_pool = SFReply.objects.filter(index=index).order_by("-id")	
	file_pool = SFContent.objects.filter(index=index, visible=True).order_by("-id")	
	for enroll in enrolls:
		works = filter(lambda w: w.student_id==enroll.student_id, works_pool)
		# 對未作答學生不特別處理，因為 filter 會傳回 []
		if len(works)>0:
			replys = filter(lambda w: w.work_id==works[-1].id, reply_pool)
			files = filter(lambda w: w.student_id==enroll.student_id, file_pool)
			if action == "2" :
			  if works[-1].score == 5:
					datas.append([enroll, works, replys, files])
			else :
				datas.append([enroll, works, replys, files])
		else :
			replys = []
			if not action == "2" :
				files = filter(lambda w: w.student_id==enroll.student_id, file_pool)		
				datas.append([enroll, works, replys, files])
	def getKey(custom):
		if custom[1]:
			if action == "3":
				return custom[1][-1].like_count
			elif action == "2":
				return custom[1][-1].score, custom[1][0].publication_date		
			elif action == "1":
				return -custom[0].seat
			else :
				return custom[1][0].reply_date, -custom[0].seat			
		else:
			return -custom[0].seat
	datas = sorted(datas, key=getKey, reverse=True)	

	return render_to_response('student/forum_memo.html', {'action':action, 'replys':replys, 'datas': datas, 'contents':contents, 'teacher_id':teacher_id, 'subject':subject, 'classroom_id':classroom_id, 'index':index, 'is_teacher':is_teacher(classroom_id, request.user.id)}, context_instance=RequestContext(request))
	
def forum_history(request, user_id, index, classroom_id):
		work = []
		contents = FContent.objects.filter(forum_id=index).order_by("-id")
		works = SFWork.objects.filter(index=index, student_id=user_id).order_by("-id")
		files = SFContent.objects.filter(index=index, student_id=user_id).order_by("-id")
		forum = FWork.objects.get(id=index)
		if len(works)> 0 :
			if works[0].publish or user_id==str(request.user.id) or is_teacher(classroom_id, request.user.id):
				return render_to_response('student/forum_history.html', {'forum': forum, 'classroom_id':classroom_id, 'works':works, 'contents':contents, 'files':files, 'index':index}, context_instance=RequestContext(request))
		return redirect("/")
			
def forum_like(request):
    forum_id = request.POST.get('forumid')  
    user_id = request.POST.get('userid')
    action = request.POST.get('action')
    likes = []
    sfworks = []
    if forum_id:
        try:
            sfworks = SFWork.objects.filter(index=forum_id, student_id=user_id)
            sfwork = sfworks[0]
            jsonDec = json.decoder.JSONDecoder()
            if action == "like":
                if sfwork.likes:
                    likes = jsonDec.decode(sfwork.likes)                     
                    if not request.user.id in likes:
                        likes.append(request.user.id)
                else:
                    likes.append(request.user.id)
                sfwork.likes = json.dumps(likes)
                sfwork.like_count = len(likes)								
                sfwork.save()
                update_avatar(request.user.id, 2, 0.1)
            else:
                if sfwork.likes:
                    likes = jsonDec.decode(sfwork.likes)
                    if request.user.id in likes:
                        likes.remove(request.user.id)
                        sfwork.likes = json.dumps(likes)
                        sfwork.like_count = len(likes)
                        sfwork.save()
                        #積分 
                        update_avatar(request.user.id, 2, -0.1)
               
        except ObjectDoesNotExist:
            sfworks = []            
        
        return JsonResponse({'status':'ok', 'likes':sfworks[0].likes}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)        

def forum_reply(request):
    index = request.POST.get('index')  
    user_id = request.POST.get('userid')
    work_id = request.POST.get('workid')		
    text = request.POST.get('reply')
    if index:       
        reply = SFReply(index=index, work_id=work_id, user_id=user_id, memo=text, publication_date=timezone.now())
        reply.save()
        sfwork = SFWork.objects.get(id=work_id)
        sfwork.reply_date = timezone.now()
        sfwork.save()
        update_avatar(request.user.id, 3, 0.2)				
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)        

			
def forum_guestbook(request):
    work_id = request.POST.get('workid')  
    guestbooks = "<table class=table>"
    if work_id:
        try :
            replys = SFReply.objects.filter(work_id=work_id).order_by("-id")
        except ObjectDoesNotExist:
            replys = []
        for reply in replys:
            user = User.objects.get(id=reply.user_id)
            guestbooks += '<tr><td nowrap>' + user.first_name + '</td><td>' + reply.memo + "</td></tr>"
        guestbooks += '</table>'
        return JsonResponse({'status':'ok', 'replys': guestbooks}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)        
			
def forum_people(request):
    forum_id = request.POST.get('forumid')  
    user_id = request.POST.get('userid')
    likes = []
    sfworks = []
    names = []
    if forum_id:
        try:
            sfworks = SFWork.objects.filter(index=forum_id, student_id=user_id).order_by("id")
            sfwork = sfworks[0]
            jsonDec = json.decoder.JSONDecoder()
            if sfwork.likes:
                likes = jsonDec.decode(sfwork.likes)  
                for like in reversed(likes):
                  user = User.objects.get(id=like)
                  names.append('<button type="button" class="btn btn-default">'+user.first_name+'</button>')
        except ObjectDoesNotExist:
            sfworks = []                   
        return JsonResponse({'status':'ok', 'likes':names}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)        

def forum_score(request):
    work_id = request.POST.get('workid')  
    score = request.POST.get('score')
    if work_id:
        sfwork = SFWork.objects.get(id=work_id)
        sfwork.score = score
        sfwork.scorer = request.user.id
        sfwork.save()
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)        

# 統計某討論主題所有同學心得
def forum_jieba(request, classroom_id, index): 
    classroom = Classroom.objects.get(id=classroom_id)
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    works = []
    contents = FContent.objects.filter(forum_id=index).order_by("-id")
    fwork = FWork.objects.get(id=index)
    teacher_id = fwork.teacher_id
    subject = fwork.title
    memo = ""
    for enroll in enrolls:
        try:
            works = SFWork.objects.filter(index=index, student_id=enroll.student_id).order_by("-id")
            if works:
                memo += works[0].memo
        except ObjectDoesNotExist:
            pass
    memo = memo.rstrip('\r\n')
    seglist = jieba.cut(memo, cut_all=False)
    hash = {}
    for item in seglist: 
        if item in hash:
            hash[item] += 1
        else:
            hash[item] = 1
    words = []
    count = 0
    error=""
    for key, value in sorted(hash.items(), key=lambda x: x[1], reverse=True):
        if ord(key[0]) > 32 :
            count += 1	
            words.append([key, value])
            if count == 100:
                break       
    return render_to_response('student/forum_jieba.html', {'index': index, 'words':words, 'enrolls':enrolls, 'classroom':classroom, 'subject':subject}, context_instance=RequestContext(request))

# 查詢某班某詞句心得
def forum_word(request, classroom_id, index, word):
        enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
        work_ids = []
        datas = []
        pos = word.index(' ')
        word = word[0:pos]
        for enroll in enrolls:
            try:
                works = SFWork.objects.filter(index=index, student_id=enroll.student_id,memo__contains=word).order_by("-id")
                if works:
                    work_ids.append(works[0].id)
                    datas.append([works[0], enroll.seat])
            except ObjectDoesNotExist:
                pass
        classroom = Classroom.objects.get(id=classroom_id)
        for work, seat in datas:
            work.memo = work.memo.replace(word, '<font color=red>'+word+'</font>')          
        return render_to_response('student/forum_word.html', {'word':word, 'datas':datas, 'classroom':classroom}, context_instance=RequestContext(request))
		
# 下載檔案
def forum_download(request, file_id):
    content = SFContent.objects.get(id=file_id)
    filename = content.title
    download =  settings.BASE_DIR + "/static/upload/" + content.filename
    wrapper = FileWrapper(file( download, "r" ))
    response = HttpResponse(wrapper, content_type = 'application/force-download')
    #response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename.encode('utf8'))
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
	
# 顯示圖片
def forum_showpic(request, file_id):
        content = SFContent.objects.get(id=file_id)
        return render_to_response('student/forum_showpic.html', {'content':content}, context_instance=RequestContext(request))

# ajax刪除檔案
def forum_file_delete(request):
    file_id = request.POST.get('fileid')  
    if file_id:
        try:
            file = SFContent.objects.get(id=file_id)
            file.visible = False
            file.delete_date = timezone.now()
            file.save()
        except ObjectDoesNotExist:
            file = []           
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)        

# 列出所有公告
class AnnounceListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'student/announce_list.html'    
    paginate_by = 20
    def get_queryset(self):

        # 記錄系統事件
        if is_event_open(self.request) :    
            log = Log(user_id=self.request.user.id, event='查看班級公告')
            log.save()        
        queryset = Message.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(AnnounceListView, self).get_context_data(**kwargs)
        context['classroom'] = Classroom.objects.get(id=self.kwargs['classroom_id'])
        return context	    

    # 限本班任課教師        
    def render_to_response(self, context):
        if not is_teacher(self.kwargs['classroom_id'], self.request.user.id ):
            if not is_assistant(self.kwargs['classroom_id'], self.request.user.id ):
              if not is_classmate(self.kwargs['classroom_id'], self.request.user.id ):
                  return redirect('/')
        return super(AnnounceListView, self).render_to_response(context)   
			

'''
--------------------思辨區
'''
# 列出所有討論主題
class SpeculationListView(ListView):
    model = SSpeculationWork
    context_object_name = 'works'
    template_name = 'student/speculation_list.html'    
    
    def get_queryset(self):
        queryset = []
        fclass_dict = dict(((fclass.forum_id, fclass) for fclass in SpeculationClass.objects.filter(classroom_id=self.kwargs['classroom_id'])))	
        #fclasses = FClass.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")
        fworks = SpeculationWork.objects.filter(id__in=fclass_dict.keys()).order_by("-id")
        sfwork_pool = SSpeculationWork.objects.filter(student_id=self.request.user.id).order_by("-id")
        for fwork in fworks:
            sfworks = filter(lambda w: w.index==fwork.id, sfwork_pool)
            if len(sfworks)> 0 :
                queryset.append([fwork, sfworks[0].publish, fclass_dict[fwork.id], len(sfworks)])
            else :
                queryset.append([fwork, False, fclass_dict[fwork.id], 0])
        def getKey(custom):
            return custom[2].publication_date, custom[2].forum_id
        queryset = sorted(queryset, key=getKey, reverse=True)	
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(SpeculationListView, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        context['bookmark'] =  self.kwargs['bookmark']
        context['fclasses'] = dict(((fclass.forum_id, fclass) for fclass in FClass.objects.filter(classroom_id=self.kwargs['classroom_id'])))
        return context	    

    # 限本班同學
    def render_to_response(self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(SpeculationListView, self).render_to_response(context)    


def speculation_submit(request, classroom_id, index):
        scores = []
        works = SSpeculationWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
        contents = SpeculationContent.objects.filter(forum_id=index)
        fwork = SpeculationWork.objects.get(id=index)
        types = SpeculationAnnotation.objects.filter(forum_id=index)
        if request.method == 'POST':
            form = SpeculationSubmitForm(request.POST, request.FILES)
            #第一次上傳加上積分
            works = SSpeculationWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
            publish = False
            if len(works)==0:
                update_avatar(request.user.id, 1, 2)
            else:
                publish = works[0].publish
            work = SSpeculationWork(index=index, student_id=request.user.id, publish=publish)
            work.save()
            if request.FILES:
                content = SSpeculationContent(index=index, student_id=request.user.id)
                myfile =  request.FILES.get("file", "")
                fs = FileSystemStorage()
                filename = uuid4().hex
                content.title = myfile.name
                content.work_id = work.id
                content.filename = str(request.user.id)+"/"+filename
                fs.save("static/upload/"+str(request.user.id)+"/"+filename, myfile)
                content.save()
            if form.is_valid():
                work.memo=form.cleaned_data['memo']
                work.save()
                if not works:
                    return redirect("/student/speculation/publish/"+classroom_id+"/"+index+"/2")	
                elif not works[0].publish:
                    return redirect("/student/speculation/publish/"+classroom_id+"/"+index+"/2")
                return redirect("/student/speculation/annotate/"+classroom_id+"/"+index+"/"+str(request.user.id))
            else:
                return render_to_response('student/speculation_form.html', {'error':form.errors}, context_instance=RequestContext(request))
        else:
            if not works.exists():
                work = SSpeculationWork(index=0, publish=False)
                form = SpeculationSubmitForm()
            else:
                work = works[0]
                form = SpeculationSubmitForm()
            files = SSpeculationContent.objects.filter(index=index, student_id=request.user.id,visible=True).order_by("-id")
            subject = SpeculationWork.objects.get(id=index).title
        return render_to_response('student/speculation_form.html', {'classroom_id':classroom_id, 'subject':subject, 'files':files, 'index': index, 'fwork':fwork, 'works':works, 'work':work, 'form':form, 'scores':scores, 'index':index, 'contents':contents, 'types': types}, context_instance=RequestContext(request))

# 發表心得
def speculation_publish(request, classroom_id, index, action):
    if action == "1":
        try:
            works = SSpeculationWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
            work = works[0]
            work.publish = True
            work.save()
        except ObjectDoesNotExist:
            pass
        return redirect("/student/speculation/annotate/"+classroom_id+"/"+index+"/"+str(request.user.id))
    elif action == "0":
        return redirect("/student/speculation/annotate/"+classroom_id+"/"+index+"/"+str(request.user.id))
    else :
        return render_to_response('student/speculation_publish.html', {'classroom_id': classroom_id, 'index': index}, context_instance=RequestContext(request))
	
			
# 列出班級思辨
class SpeculationAnnotateView(ListView):
    model = SSpeculationWork
    context_object_name = 'works'
    template_name = 'student/speculation_annotate.html'    
    
    def get_queryset(self):
        works = SSpeculationWork.objects.filter(index=self.kwargs['index'], student_id=self.kwargs['id']).order_by("-id")          	
        return works
        
    def get_context_data(self, **kwargs):
        context = super(SpeculationAnnotateView, self).get_context_data(**kwargs)        
        ids = []
        queryset = []
        enrolls = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("seat")
        for enroll in enrolls :
            ids.append(enroll.student_id)
        work_pool = SSpeculationWork.objects.filter(student_id__in=ids).order_by("-id")
        for enroll in enrolls:
            works = filter(lambda w: w.student_id==enroll.student_id, work_pool)
            if len(works)> 0:
                queryset.append([enroll, works[0].publish])
            else:
                queryset.append([enroll, False])
        context['queryset'] = queryset
        context['classroom_id'] = self.kwargs['classroom_id']
        context['student_id'] = int(self.kwargs['id'])
        context['enrolls'] = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("seat")
        context['swork'] = SpeculationWork.objects.get(id=self.kwargs['index'])
        context['contents'] = SpeculationContent.objects.filter(forum_id=self.kwargs['index'])
        context['files'] = SSpeculationContent.objects.filter(index=self.kwargs['index'], student_id=self.kwargs['id'])
        context['types'] = SpeculationAnnotation.objects.filter(forum_id=self.kwargs['index'])
        context['index'] = self.kwargs['index']
        return context	    

    # 限本班同學
    def render_to_response(self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(SpeculationAnnotateView, self).render_to_response(context)    

# 列出班級思辨
class SpeculationAnnotateClassView(ListView):
    model = SSpeculationWork
    context_object_name = 'annotations'
    template_name = 'student/speculation_annotate_class.html'    
    
    def get_queryset(self):
        annotations = SpeculationAnnotation.objects.filter(forum_id=self.kwargs['index'])
        return annotations
        
    def get_context_data(self, **kwargs):
        context = super(SpeculationAnnotateClassView, self).get_context_data(**kwargs)        
        context['classroom_id'] = self.kwargs['classroom_id']
        context['annotate_id'] = int(self.kwargs['id'])
        context['enrolls'] = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id'])
        context['swork'] = SpeculationWork.objects.get(id=self.kwargs['index'])
        context['contents'] = SpeculationContent.objects.filter(forum_id=self.kwargs['index'])
        context['types'] = SpeculationAnnotation.objects.filter(forum_id=self.kwargs['index'])
        context['index'] = self.kwargs['index']
        return context	    

    # 限本班同學
    def render_to_response(self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        if self.kwargs['id'] == "0":
            annotations = SpeculationAnnotation.objects.filter(forum_id=self.kwargs['index'])
            if len(annotations)>0:
                return redirect("/student/speculation/annotateclass/"+self.kwargs['classroom_id']+"/"+self.kwargs['index']+"/"+str(annotations[0].id))
        return super(SpeculationAnnotateClassView, self).render_to_response(context)    

			
# 下載檔案
def speculation_download(request, file_id):
    content = SSpeculationContent.objects.get(id=file_id)
    filename = content.title
    download =  settings.BASE_DIR + "/static/upload/" + content.filename
    wrapper = FileWrapper(file( download, "r" ))
    response = HttpResponse(wrapper, content_type = 'application/force-download')
    #response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename.encode('utf8'))
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
	
# 顯示圖片
def speculation_showpic(request, file_id):
        content = SSpeculationContent.objects.get(id=file_id)
        return render_to_response('student/forum_showpic.html', {'content':content}, context_instance=RequestContext(request))

