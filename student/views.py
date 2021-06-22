# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, CreateView
from student.models import *
from teacher.models import *
from account.models import *
from student.forms import *
from django.core.exceptions import ObjectDoesNotExist,  MultipleObjectsReturned
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
import os

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
        classroom_ids = []
        #教師班級
        if self.kwargs['role'] == "1":
            classrooms = Classroom.objects.filter(teacher_id=self.request.user.id)
            for classroom in classrooms:
                classroom_ids.append(classroom.id)
            enrolls = Enroll.objects.filter(classroom_id__in=classroom_ids, student_id=self.request.user.id).order_by("-id")
        elif self.kwargs['role'] == "2":
            assistants = Assistant.objects.filter(user_id=self.request.user.id)
            for assistant in assistants:
                classroom_ids.append(assistant.classroom_id)
            enrolls = Enroll.objects.filter(classroom_id__in=classroom_ids, student_id=self.request.user.id).order_by("-id")
        else :
            enrolls = Enroll.objects.filter(student_id=self.request.user.id, seat__gt=0).order_by("-id")
        for enroll in enrolls:
            queryset.append([enroll, Classroom.objects.get(id=enroll.classroom_id).teacher_id])
        return queryset         			
			
    def get_context_data(self, **kwargs):
        context = super(ClassroomListView, self).get_context_data(**kwargs)
        context['role'] = self.kwargs['role']
        return context	
    
# 查看可加入的班級
class ClassroomAddListView(ListView):
    context_object_name = 'classroom_teachers'
    paginate_by = 20
    template_name = 'student/classroom_add.html'
    
    def get_queryset(self):        
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
        return render(request,'student/classroom_add.html', {'classroom_teachers':classroom_teachers})
    
# 加入班級
def classroom_enroll(request, classroom_id):
        scores = []
        if request.method == 'POST':
                form = EnrollForm(request.POST)
                if form.is_valid():
                    try:
                        classroom = Classroom.objects.get(id=classroom_id)
                        if classroom.password == form.cleaned_data['password']:
                                try:
                                    enroll = Enroll.objects.get(classroom_id=classroom_id, student_id=request.user.id)
                                    return redirect("/student/classroom/0")
                                except ObjectDoesNotExist:
                                    enroll = Enroll(classroom_id=classroom_id, student_id=request.user.id, seat=form.cleaned_data['seat'])
                                    enroll.save()                                
                                messages = Message.objects.filter(author_id=classroom.teacher_id, classroom_id=classroom_id)	 
                                for message in messages:
                                    messagepoll = MessagePoll(message_type=1, message_id=message.id, reader_id=request.user.id, classroom_id=classroom_id)
                                    messagepoll.save()	
                        else:
                                return render(request,'message.html', {'message':"選課密碼錯誤"})
                      
                    except Classroom.DoesNotExist:
                        pass
                    
                    
                    return redirect("/student/classroom/0")
        else:
            form = EnrollForm()
        return render(request,'student/classroom_enroll.html', {'form':form})
        
# 修改座號
def seat_edit(request, enroll_id, classroom_id):
    enroll = Enroll.objects.get(id=enroll_id)
    if request.method == 'POST':
        form = SeatForm(request.POST)
        if form.is_valid():
            enroll.seat =form.cleaned_data['seat']
            enroll.save()
            classroom_name = Classroom.objects.get(id=classroom_id).name
            return redirect('/student/classroom/'+classroom_id)
    else:
        form = SeatForm(instance=enroll)

    return render(request,'form.html',{'form': form})  



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
        return render(request,'student/classmate.html', {'classroom':classroom, 'enrolls':enroll_group})

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
    def render(request,self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(ForumListView, self).render(request,context)    

# 發表心得
def forum_publish(request, classroom_id, index, action):
    if action == "1":
        try:
            fwork = FWork.objects.get(id=index)
            works = SFWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
            work = works[0]
            work.publish = True
            work.save()
            update_avatar(request.user.id, 1, 2)
            # History
            history = PointHistory(user_id=request.user.id, kind=1, message=u'2分--繳交討論區作業<'+fwork.title+'>', url='/student/forum/memo/'+classroom_id+'/'+index+'/'+action)
            history.save()								
        except ObjectDoesNotExist:
            pass
        return redirect("/student/forum/memo/"+classroom_id+"/"+index+"/0")
    elif action == "0":
        return redirect("/student/forum/memo/"+classroom_id+"/"+index+"/0")
    else :
        return render(request,'student/forum_publish.html', {'classroom_id': classroom_id, 'index': index})
	

def forum_submit(request, classroom_id, index):
        scores = []
        works = SFWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
        contents = FContent.objects.filter(forum_id=index).order_by("id")
        fwork = FWork.objects.get(id=index)
        if request.method == 'POST':
            form = ForumSubmitForm(request.POST, request.FILES)
            #第一次上傳加上積分
            works = SFWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
            work = SFWork(index=index, student_id=request.user.id, publish=False)
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
                work.memo_e = form.cleaned_data['memo_e']
                work.memo_c = form.cleaned_data['memo_c']								
                work.save()
                if not works:
                    return redirect("/student/forum/publish/"+classroom_id+"/"+index+"/2")	
                elif not works[0].publish:
                    return redirect("/student/forum/publish/"+classroom_id+"/"+index+"/2")
                return redirect("/student/forum/memo/"+classroom_id+"/"+index+"/0")
            else:
                return render(request,'student/forum_form.html', {'error':form.errors})
        else:
            if not works.exists():
                work = SFWork(index=0, publish=False)
                form = ForumSubmitForm()
            else:
                work = works[0]
                form = ForumSubmitForm()
            files = SFContent.objects.filter(index=index, student_id=request.user.id,visible=True).order_by("-id")
            subject = FWork.objects.get(id=index).title
        return render(request,'student/forum_form.html', {'classroom_id':classroom_id, 'subject':subject, 'files':files, 'index': index, 'fwork':fwork, 'works':works, 'work':work, 'form':form, 'scores':scores, 'index':index, 'contents':contents})

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
		if len(works)> 0:
			work_new = works[0]
			work_first = works.last()
			publish = work_first.publish
			replys = SFReply.objects.filter(index=index, work_id=work_first.id).order_by("-id")	
			files = SFContent.objects.filter(index=index, student_id=user_id, visible=True).order_by("-id")	
		else :
			work_new = SFWork(index=index, student_id=user_id)
			work_first = SFWork(index=index, student_id=user_id)			
		return render(request,'student/forum_show.html', {'work_new': work_new, 'work_first':work_first, 'publish':publish, 'classroom_id':classroom_id, 'contents':contents, 'replys':replys, 'files':files, 'forum':forum, 'user_id':user_id, 'teacher_id':teacher_id, 'works': works, 'is_teacher':is_teacher(classroom_id, request.user.id)})
		
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

	return render(request,'student/forum_memo.html', {'action':action, 'replys':replys, 'datas': datas, 'contents':contents, 'teacher_id':teacher_id, 'subject':subject, 'classroom_id':classroom_id, 'index':index, 'is_teacher':is_teacher(classroom_id, request.user.id)})
	
def forum_history(request, user_id, index, classroom_id):
		work = []
		contents = FContent.objects.filter(forum_id=index).order_by("-id")
		works = SFWork.objects.filter(index=index, student_id=user_id).order_by("-id")
		files = SFContent.objects.filter(index=index, student_id=user_id).order_by("-id")
		forum = FWork.objects.get(id=index)
		if len(works)> 0 :
			if works[0].publish or user_id==str(request.user.id) or is_teacher(classroom_id, request.user.id):
				return render(request,'student/forum_history.html', {'forum': forum, 'classroom_id':classroom_id, 'works':works, 'contents':contents, 'files':files, 'index':index})
		return redirect("/")
			
def forum_like(request):
    forum_id = request.POST.get('forumid')  
    classroom_id = request.POST.get('classroomid')  		
    user_id = request.POST.get('userid')
    action = request.POST.get('action')
    likes = []
    sfworks = []
    fwork = FWork.objects.get(id=forum_id)
    user = User.objects.get(id=user_id)
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
                # History
                history = PointHistory(user_id=request.user.id, kind=2, message=u'+0.1分--討論區按讚<'+fwork.title+'><'+user.first_name+'>', url="/student/forum/memo/"+classroom_id+"/"+forum_id+"/0/#"+user_id)
                history.save()										
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
                        # History
                        history = PointHistory(user_id=request.user.id, kind=2, message=u'-0.1分--討論區按讚取消<'+fwork.title+'><'+user.first_name+'>', url="/student/forum/memo/"+classroom_id+"/"+forum_id+"/0/#"+user_id)
                        history.save()		               
        except ObjectDoesNotExist:
            sfworks = []            
        
        return JsonResponse({'status':'ok', 'likes':sfworks[0].likes}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)        

def forum_reply(request):
    forum_id = request.POST.get('forumid')  
    classroom_id = request.POST.get('classroomid')		
    user_id = request.POST.get('userid')
    work_id = request.POST.get('workid')		
    text = request.POST.get('reply')
    fwork = FWork.objects.get(id=forum_id)
    user = User.objects.get(id=user_id)
    if forum_id:       
        reply = SFReply(index=forum_id, work_id=work_id, user_id=user_id, memo=text, publication_date=timezone.now())
        reply.save()
        sfwork = SFWork.objects.get(id=work_id)
        sfwork.reply_date = timezone.now()
        sfwork.save()
        update_avatar(request.user.id, 3, 0.2)
        # History
        history = PointHistory(user_id=request.user.id, kind=3, message=u'0.2分--討論區留言<'+fwork.title+'><'+user.first_name+'>', url='/student/forum/memo/'+classroom_id+'/'+forum_id+'/0/#'+user_id)
        history.save()		              
				
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
    classroom_id = request.POST.get('classroomid')  
    user_id = request.POST.get('userid')  		
    score = request.POST.get('score')
    comment = request.POST.get('comment')		
    if work_id and is_teacher(classroom_id, request.user.id):
        sfwork = SFWork.objects.get(id=work_id)
        sfwork.score = score
        sfwork.comment = comment
        sfwork.scorer = request.user.id
        sfwork.comment_publication_date = timezone.now()
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
    return render(request,'student/forum_jieba.html', {'index': index, 'words':words, 'enrolls':enrolls, 'classroom':classroom, 'subject':subject})

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
        return render(request,'student/forum_word.html', {'word':word, 'datas':datas, 'classroom':classroom})
		
# 下載檔案
def forum_download(request, file_id):
    content = SFContent.objects.get(id=file_id)
    filename = content.title
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))		
    download =  BASE_DIR + "/static/upload/" + content.filename
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
        return render(request,'student/forum_showpic.html', {'content':content})

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
        queryset = Message.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(AnnounceListView, self).get_context_data(**kwargs)
        context['classroom'] = Classroom.objects.get(id=self.kwargs['classroom_id'])
        return context	    

    # 限本班任課教師        
    def render(request,self, context):
        if not is_teacher(self.kwargs['classroom_id'], self.request.user.id ):
            if not is_assistant(self.kwargs['classroom_id'], self.request.user.id ):
              if not is_classmate(self.kwargs['classroom_id'], self.request.user.id ):
                  return redirect('/')
        return super(AnnounceListView, self).render(request,context)   
			

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
    def render(request,self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(SpeculationListView, self).render(request,context)    


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
                return render(request,'student/speculation_form.html', {'error':form.errors})
        else:
            if not works.exists():
                work = SSpeculationWork(index=0, publish=False)
                form = SpeculationSubmitForm()
            else:
                work = works[0]
                form = SpeculationSubmitForm()
            files = SSpeculationContent.objects.filter(index=index, student_id=request.user.id,visible=True).order_by("-id")
            subject = SpeculationWork.objects.get(id=index).title
        return render(request,'student/speculation_form.html', {'classroom_id':classroom_id, 'subject':subject, 'files':files, 'index': index, 'fwork':fwork, 'works':works, 'work':work, 'form':form, 'scores':scores, 'index':index, 'contents':contents, 'types': types})

# 發表心得
def speculation_publish(request, classroom_id, index, action):
    if action == "1":
        try:
            works = SSpeculationWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
            work = works[0]
            work.publish = True
            work.save()
            update_avatar(request.user.id, 1, 2)
            # History
            fwork = FWork.objects.get(id=index)
            history = PointHistory(user_id=request.user.id, kind=1, message=u'2分--繳交思辨區作業<'+fwork.title+'>', url='/student/speculation/annotate/'+classroom_id+'/'+index+'/'+str(request.user.id))
            history.save()							
        except ObjectDoesNotExist:
            pass
        return redirect("/student/speculation/annotate/"+classroom_id+"/"+index+"/"+str(request.user.id))
    elif action == "0":
        return redirect("/student/speculation/annotate/"+classroom_id+"/"+index+"/"+str(request.user.id))
    else :
        return render(request,'student/speculation_publish.html', {'classroom_id': classroom_id, 'index': index})
	
			
# 列出班級思辨
class SpeculationAnnotateView(ListView):
    model = SSpeculationWork
    context_object_name = 'works'
    template_name = 'student/speculation_annotate.html'    
    
    def get_queryset(self):
        works = SSpeculationWork.objects.filter(index=self.kwargs['index'], student_id=self.kwargs['id']).order_by("-id")          	
        works = list(works)
        return works
        
    def get_context_data(self, **kwargs):
        context = super(SpeculationAnnotateView, self).get_context_data(**kwargs)        
        ids = []
        queryset = []
        enrolls = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("seat")
        for enroll in enrolls :
            ids.append(enroll.student_id)
        work_pool = SSpeculationWork.objects.filter(index=self.kwargs['index'], student_id__in=ids).order_by("-id")
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
    def render(request,self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(SpeculationAnnotateView, self).render(request,context)    

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
    def render(request,self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        if self.kwargs['id'] == "0":
            annotations = SpeculationAnnotation.objects.filter(forum_id=self.kwargs['index'])
            if len(annotations)>0:
                return redirect("/student/speculation/annotateclass/"+self.kwargs['classroom_id']+"/"+self.kwargs['index']+"/"+str(annotations[0].id))
        return super(SpeculationAnnotateClassView, self).render(request,context)    

			
# 下載檔案
def speculation_download(request, file_id):
    content = SSpeculationContent.objects.get(id=file_id)
    filename = content.title
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))		
    download =  BASE_DIR + "/static/upload/" + content.filename
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
        return render(request,'student/forum_showpic.html', {'content':content})

# 列出組別
class GroupListView(ListView):
    model = ClassroomGroup
    context_object_name = 'groups'
    paginate_by = 30
    template_name = 'student/group.html'
    
    def get_queryset(self):
        queryset = ClassroomGroup.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")
        return queryset         			

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)        
        context['classroom_id'] = self.kwargs['classroom_id']
        return context	    			

def speculation_score(request):
    work_id = request.POST.get('workid')  
    classroom_id = request.POST.get('classroomid')  
    user_id = request.POST.get('userid')  		
    score = request.POST.get('score')
    comment = request.POST.get('comment')		
    if work_id and is_teacher(classroom_id, request.user.id):
        sfwork = SSpeculationWork.objects.get(id=work_id)
        sfwork.score = score
        sfwork.comment = comment
        sfwork.scorer = request.user.id
        sfwork.comment_publication_date = timezone.now()
        sfwork.save()
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':1}, safe=False)        

		
# 顯示所有組別
def group_list(request, group_id):
        groups = []
        student_groups = {}
        enroll_list = []
        group_list = {}
        group_ids = []
        group = ClassroomGroup.objects.get(id=group_id)
        numbers = group.numbers
        enrolls = Enroll.objects.filter(classroom_id=group.classroom_id).order_by("seat")
        for enroll in enrolls:
            enroll_list.append(enroll.id)
        enroll_groups = StudentGroup.objects.filter(enroll_id__in=enroll_list, group_id=group_id)
        for enroll_group in enroll_groups:
            group_ids.append(enroll_group.enroll_id)
            group_list[enroll_group.enroll_id] = enroll_group.group
            enroll = Enroll.objects.get(id=enroll_group.enroll_id)
            if enroll_group.group in student_groups:
                student_groups[enroll_group.group].append(enroll)
            else:
                student_groups[enroll_group.group]=[enroll]	            
        for i in range(numbers):
            try: 
                leader_id = StudentGroupLeader.objects.get(group_id=group_id, group=i).enroll_id
                leader = Enroll.objects.get(id=leader_id)
            except ObjectDoesNotExist:
                leader_id = 0
                leader = None
            if i in student_groups:
                groups.append([i, student_groups[i], leader])
            else:
                groups.append([i, [], leader])
					
        #找出尚未分組的學生
        no_group = []
        for enroll in enrolls:
            if not enroll.id in group_ids:
                no_group.append([enroll.seat, enroll.student])
    
        enroll_user = Enroll.objects.get(student_id=request.user.id, classroom_id=group.classroom_id)
        try:
            user_group = StudentGroup.objects.get(group_id=group_id, enroll_id=enroll_user.id).group
        except ObjectDoesNotExist:
            user_group = -1
        return render(request,'student/group_join.html', {'user_group':user_group, 'group':group, 'groups':groups, 'enroll_id':enroll_user.id, 'student_groups':student_groups, 'no_group':no_group, 'classroom_id':group.classroom_id, 'group_id':group_id})

			
# 顯示所有組別
def group_join(request, group_id, number, enroll_id):
    try:
        group = StudentGroup.objects.get(group_id=group_id, enroll_id=enroll_id)
        group.group = number
    except ObjectDoesNotExist:
        group = StudentGroup(group_id=group_id, enroll_id=enroll_id, group=number)
    if ClassroomGroup.objects.get(id=group_id).opening:
        group.save()
    StudentGroupLeader.objects.filter(group_id=group_id, enroll_id=enroll_id).delete()
			
    return redirect("/student/group/list/"+group_id)

# 設為組長
def group_leader(request, group_id, number, enroll_id):
    try:
        group = StudentGroupLeader.objects.get(group_id=group_id, group=number)
        group.enroll_id = enroll_id
    except ObjectDoesNotExist:
        group = StudentGroupLeader(group_id=group_id, enroll_id=enroll_id, group=number)
    if ClassroomGroup.objects.get(id=group_id).opening:
        group.save()			
			
    return redirect("/student/group/list/"+group_id)


# 列出所有討論測驗
class ExamListView(ListView):
    model = Exam
    context_object_name = 'exams'
    template_name = 'student/exam_list.html'    
    
    def get_queryset(self):
        queryset = []
        examclass_dict = dict(((examclass.exam_id, examclass) for examclass in ExamClass.objects.filter(classroom_id=self.kwargs['classroom_id'])))	
        #fclasses = FClass.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")
        exams = Exam.objects.filter(id__in=examclass_dict.keys()).order_by("-id")
        examwork_pool = ExamWork.objects.filter(student_id=self.request.user.id).order_by("-id")
        for exam in exams:
            questions = ExamQuestion.objects.filter(exam_id=exam.id)					
            examworks = filter(lambda w: w.exam_id==exam.id, examwork_pool)
            retest = False
            examclass = examclass_dict[exam.id]
            if len(examworks) < examclass.round_limit or examclass.round_limit == 0 :
                retest = True
            if len(examworks)> 0 :
                queryset.append([exam, examworks[0].publish, examclass_dict[exam.id], examworks, len(questions), examclass_dict[exam.id], retest])
            else :
                queryset.append([exam, False, examclass_dict[exam.id], 0, len(questions), examclass_dict[exam.id], retest])
        def getKey(custom):
            return custom[2].publication_date, custom[2].exam_id
        queryset = sorted(queryset, key=getKey, reverse=True)	
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(ExamListView, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        context['examclasses'] = dict(((examclass.exam_id, examclass) for examclass in ExamClass.objects.filter(classroom_id=self.kwargs['classroom_id'])))
        return context	    

    # 限本班同學
    def render(request,self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(ExamListView, self).render(request,context)    	
			
def exam_question(request, classroom_id, exam_id, examwork_id, question_id):	
    exam = Exam.objects.get(id=exam_id)
    examworks = ExamWork.objects.filter(exam_id=exam_id, student_id=request.user.id).order_by("-id")

    if len(examworks)> 0:
        if examworks[0].publish:
            questions = ExamQuestion.objects.filter(exam_id=exam_id).order_by("?")
            question_ids = []		
            for question in questions:
                question_ids.append(question.id)
            question_string = ",".join(str(question_id) for question_id in question_ids)			
            examwork = ExamWork(exam_id=exam_id, student_id=request.user.id, questions=question_string)
        else :
            examwork = examworks[0]
    else :
        questions = ExamQuestion.objects.filter(exam_id=exam_id).order_by("?")
        question_ids = []		
        for question in questions:
            question_ids.append(question.id)
        question_string = ",".join(str(question_id) for question_id in question_ids)			
        examwork = ExamWork(exam_id=exam_id, student_id=request.user.id, questions=question_string)
    examwork.save()
    questions = examwork.questions
    question_ids = questions.split(',')
    qas = []
    answer_dict = dict(((answer.question_id, answer) for answer in ExamAnswer.objects.filter(examwork_id=examwork.id, question_id__in=question_ids, student_id=request.user.id))) 
    for question in question_ids:
        question = int(question)
        if question in answer_dict:
            qas.append([question, answer_dict[question]])
        else :
            qas.append([question, 0])
    if not question_id == "0":
        question = ExamQuestion.objects.get(id=question_id)
    else :
        if len(questions)> 0 :
            return redirect('/student/exam/question/'+classroom_id+'/'+exam_id+'/'+examwork_id+'/'+str(question_ids[0]))
        else :
            return redirect('/student/exam/'+classroom_id)
    try :
        answer = ExamAnswer.objects.get(examwork_id=examwork.id, question_id=question_id, student_id=request.user.id).answer
    except ObjectDoesNotExist:
        answer = ""
    return render(request,'student/exam_question.html', {'examwork': examwork, 'answer':answer, 'exam':exam, 'qas':qas, 'question':question, 'question_id':question_id, 'classroom_id': classroom_id})
			
# Ajax 設定測驗答案
def exam_answer(request):
    examwork_id = request.POST.get('examworkid')	
    question_id = request.POST.get('questionid')
    input_answer = request.POST.get('answer')
    if examwork_id :
        question = ExamQuestion.objects.get(id=question_id)
        try:
            examwork = ExamWork.objects.get(id=examwork_id)
        except ObjectDoesNotExist:
	         examwork = ExamWork(exam_id=exam_id, student_id=request.user.id)
        if not examwork.publish :
            try :
               answer = ExamAnswer.objects.get(examwork_id=examwork_id, question_id=question_id, student_id=request.user.id) 	
            except ObjectDoesNotExist :
                answer = ExamAnswer(examwork_id=examwork_id, question_id=question_id, student_id=request.user.id)
            answer.answer = input_answer
            answer.save()
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)
	
def exam_submit(request, classroom_id, exam_id, examwork_id):
    examclass = ExamClass.objects.get(exam_id=exam_id, classroom_id=classroom_id)
    examworks = ExamWork.objects.filter(exam_id=exam_id, student_id=request.user.id)
    if examclass.round_limit == 0 or len(examworks) <= examclass.round_limit:
        try:
            examwork = ExamWork.objects.get(id=examwork_id)
        except ObjectDoesNotExist:
	          examwork = ExamWork(exam_id=exam_id, student_id=request.user.id)	
        examwork.publish = True
        examwork.publication_date = timezone.now()
        questions = ExamQuestion.objects.filter(exam_id=exam_id).order_by("id")	
        question_ids = []
        score = 0
        for question in questions:
            question_ids.append(question.id)		
        answer_dict = dict(((answer.question_id, answer.answer) for answer in ExamAnswer.objects.filter(examwork_id=examwork_id, question_id__in=question_ids, student_id=request.user.id)))		
        for question in questions:
            if question.id in answer_dict:
                if question.answer == answer_dict[question.id] :
                    score += question.score		                 
        examwork.score = score
        examwork.scorer = 0
        examwork.save()
    return redirect('/student/exam/score/'+classroom_id+'/'+exam_id+'/'+examwork_id+'/'+str(request.user.id)+'/0')

def exam_score(request, classroom_id, exam_id, examwork_id, user_id, question_id):
    score = 0
    score_total = 0
    exam = Exam.objects.get(id=exam_id)
    try:
        examwork = ExamWork.objects.get(id=examwork_id)
    except ObjectDoesNotExist:
        pass
    question_ids = examwork.questions.split(',')
    score_answer = dict(((question.id, [question.score, question.answer]) for question in ExamQuestion.objects.filter(exam_id=exam_id)))			
    qas = []
    for question in question_ids:
        score_total += score_answer[int(question)][0]
    answer_dict = dict(((answer.question_id, [answer.answer, answer.answer_right]) for answer in ExamAnswer.objects.filter(examwork_id=examwork_id, question_id__in=question_ids, student_id=user_id)))		
    for question in question_ids:
        question = int(question)
        if question in answer_dict:
            if score_answer[question][1] == answer_dict[question][0] or answer_dict[question][1]:
                score += score_answer[question][0]
            qas.append([question, score_answer[question][1], answer_dict[question]])
        else :
            qas.append([question, score_answer[question][1], []])
    if not question_id == "0":
        question = ExamQuestion.objects.get(id=question_id)
    else :
        return redirect('/student/exam/score/'+classroom_id+'/'+exam_id+'/'+examwork_id+'/'+user_id+"/"+str(question_ids[0]))
    try :
        answer = ExamAnswer.objects.get(examwork_id=examwork_id, question_id=question_id, student_id=user_id).answer
    except ObjectDoesNotExist:
        answer = 0

    return render(request,'student/exam_score.html', {'user_id':user_id, 'classroom_id':classroom_id, 'examwork': examwork, 'score_total': score_total, 'score':score, 'question':question, 'answer':answer, 'exam':exam, 'qas':qas})
			
# 點擊影片觀看記錄
def video_log(request):
    # 記錄系統事件
    message = request.POST.get('log')
    youtube_id = request.POST.get('youtube_id')
    log = Log(user_id=request.user.id, youtube_id=youtube_id, event=message)
    log.save()
    return JsonResponse({'status':'ok'}, safe=False)

# 下載檔案
def team_download(request, file_id):
    team = TeamContent.objects.get(id=file_id)
    filename = content.title
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))		
    download =  BASE_DIR + "/static/upload/" + content.filename
    wrapper = FileWrapper(file( download, "r" ))
    response = HttpResponse(wrapper, content_type = 'application/force-download')
    #response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename.encode('utf8'))
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response


# 列出所有合作任務
class TeamListView(ListView):
    model = TeamWork
    context_object_name = 'teams'
    template_name = 'student/team_list.html'    
    
    def get_queryset(self):
        queryset = []
        classroom_id = self.kwargs['classroom_id']
        works = TeamWork.objects.filter(classroom_id=classroom_id).order_by("-id")
        for work in works:
            try:
                enroll = Enroll.objects.get(classroom_id=self.kwargs['classroom_id'], student_id=self.request.user.id)
                group = TeamClass.objects.get(team_id=work.id, classroom_id=self.kwargs['classroom_id']).group
            except ObjectDoesNotExist:
                group = 0
            queryset.append([work, group])
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        context['grouping'] = self.kwargs['grouping']
        return context	    

def team_stage(request, classroom_id, grouping, team_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    enroll_dict = {}
    for enroll in enrolls:
        enroll_dict[enroll.id] = enroll
    groupclass_list = []  
    groupclass_dict = {}       
    student_ids = {}
    if grouping == "0":
        counter = 0
        for enroll in enrolls:
            groupclass_dict[counter] = [enroll_dict[enroll.id]]  
            counter +=1
    else:
        try:
            numbers = ClassroomGroup.objects.get(id=grouping).numbers
            for i in range(numbers):
                groupclass_dict[i] = []
                students = StudentGroup.objects.filter(group_id=grouping, group=i)
                for student in students:                    
                    if student.enroll_id in enroll_dict:
                        groupclass_dict[i].append(enroll_dict[student.enroll_id])            
        except ObjectDoesNotExist:
            counter = 0
            for enroll in enrolls:
                groupclass_dict[counter]= [enroll]  
                counter += 1          
    group_list = []
    for key in groupclass_dict:
        try: 
            leader_id = StudentGroupLeader.objects.get(group_id=grouping, group=key).enroll_id
            leader = Enroll.objects.get(id=leader_id)
        except ObjectDoesNotExist:
            leader_id = 0
            leader = None        
        if grouping == "0":
            teamworks = TeamContent.objects.filter(team_id=team_id, user_id=groupclass_dict[key][0].student_id, publish=True)
        else:
            members = groupclass_dict[key]
            student_ids = []
            for member in members:
                student_ids.append(member.student_id)
            teamworks = TeamContent.objects.filter(team_id=team_id, user_id__in=student_ids, publish=True)
        groupclass_list.append([key, leader, groupclass_dict[key], len(teamworks)])    

    teamclass = TeamClass.objects.get(team_id=team_id, classroom_id=classroom_id)
    try:
        group = ClassroomGroup.objects.get(id=teamclass.group)
    except ObjectDoesNotExist:
        group = ClassroomGroup(title="不分組", id=0)
    return render(request,'student/team_stage.html',{'grouping': grouping, 'groups': groupclass_list, 'team_id': team_id, 'classroom_id':classroom_id, 'published':len(teamworks)})


# 列出所有合作任務素材
class TeamContentListView(ListView):
    model = TeamContent
    context_object_name = 'contents'
    template_name = "student/team_content.html"		
    def get_queryset(self):
        if self.kwargs['grouping'] == "0":
            group_id = 0
        else:
            enrolls = StudentGroup.objects.filter(group_id=self.kwargs['grouping'], group=self.kwargs['stage'])
            group_id = enrolls[0].group
        publish = self.kwargs['publish']
        user_ids = []        
        enrolls = StudentGroup.objects.filter(group_id=self.kwargs['grouping'], group=group_id)
        if len(enrolls) > 0:           
            for enroll in enrolls:
                student_id = Enroll.objects.get(id=enroll.enroll_id).student_id
                user_ids.append(student_id)
        else:
            if self.kwargs['stage'] != "0":
                try:
                    enroll = Enroll.objects.get(id=self.kwargs['stage'])
                    user_ids.append(enroll.student_id)
                except ObjectDoesNotExist:
                    pass
            else:
                user_ids.append(self.request.user.id)       
        if publish == "0":
            queryset = TeamContent.objects.filter(team_id=self.kwargs['team_id'], user_id__in=user_ids).order_by("-id")
        else :
            queryset = TeamContent.objects.filter(team_id=self.kwargs['team_id'], user_id__in=user_ids, publish=True).order_by("-id")          
        return queryset
			
    def get_context_data(self, **kwargs):
        context = super(TeamContentListView, self).get_context_data(**kwargs)
        teamwork = TeamWork.objects.get(id=self.kwargs['team_id'])
        context['teamwork']= teamwork
        context['team_id'] = self.kwargs['team_id']
        context['grouping'] = self.kwargs['grouping']
        context['classroom_id'] = self.kwargs['classroom_id']
        if self.kwargs['grouping'] == "0":
            group_id = 0
        else :
            group_id = TeamClass.objects.get(team_id=self.kwargs['team_id'], classroom_id=self.kwargs['classroom_id']).group
        try:  
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
            leader = StudentGroupLeader.objects.get(group_id=group_id, enroll_id=enroll.id)
            mygroup = StudentGroup.objects.get(group_id=group_id, enroll_id=enroll.id)
            if leader.group == mygroup.group:
                context['leader'] = True
            else:
                context['leader'] = False
        except ObjectDoesNotExist:
            context['leader'] = False
        enroll_id = Enroll.objects.get(classroom_id=self.kwargs['classroom_id'], student_id=self.request.user.id).id
        try:
            group = StudentGroup.objects.get(enroll_id=enroll_id, group_id=group_id).group
        except ObjectDoesNotExist:
            context['leader'] = True
        return context	
            
#新增一個素材
class TeamContentCreateView(CreateView):
    model = TeamContent
    form_class = TeamContentForm
    template_name = "student/team_content_form.html"
    def form_valid(self, form):
        self.object = form.save(commit=False)
        work = TeamContent(team_id=self.object.team_id)
        if self.object.types == 1:
            work.types = 1
            work.title = self.object.title
            work.link = self.object.link
        if self.object.types  == 2:
            work.types = 2					
            work.youtube = self.object.youtube
        if self.object.types  == 3:
            work.types = 3
            myfile = self.request.FILES['content_file']
            fs = FileSystemStorage()
            filename = uuid4().hex
            work.title = myfile.name
            work.filename = str(self.request.user.id)+"/"+filename
            fs.save("static/upload/"+str(self.request.user.id)+"/"+filename, myfile)
        if self.object.types  == 4:
            work.types = 4
        work.memo = self.object.memo
        work.user_id = self.request.user.id
        work.save()         
  
        return redirect("/student/team/content/"+self.kwargs['classroom_id']+"/"+self.kwargs['grouping']+"/"+self.kwargs['team_id']+"/0/0")  

    def get_context_data(self, **kwargs):
        ctx = super(TeamContentCreateView, self).get_context_data(**kwargs)
        ctx['team'] = TeamWork.objects.get(id=self.kwargs['team_id'])
        return ctx

def team_delete(request, classroom_id, grouping,  team_id, content_id):
    instance = TeamContent.objects.get(id=content_id)
    instance.delete()

    return redirect("/student/team/content/"+classroom_id+"/"+{{gropuing}}+"/"+team_id+"/0/0")  
	
def team_edit(request, classroom_id, grouping, team_id, content_id):
    try:
        instance = TeamContent.objects.get(id=content_id)
    except:
        pass
    if request.method == 'POST':
            content_id = request.POST.get("id", "")
            try:
                content = TeamContent.objects.get(id=content_id)
            except ObjectDoesNotExist:
	              content = TeamContent(forum_id= request.POST.get("forum_id", ""), types=form.cleaned_data['types'])
            if content.types == 1:
                content.title = request.POST.get("title", "")
                content.link = request.POST.get("link", "")
            elif content.types == 2:
                content.youtube = request.POST.get("youtube", "")
            elif content.types == 3:
                myfile =  request.FILES.get("content_file", "")
                fs = FileSystemStorage()
                filename = uuid4().hex
                content.title = myfile.name
                content.filename = str(request.user.id)+"/"+filename
                fs.save("static/upload/"+str(request.user.id)+"/"+filename, myfile)
            content.memo = request.POST.get("memo", "")
            content.save()
            return redirect('/student/team/content/'+classroom_id+'/'+grouping+"/"+team_id+"/0/0")   
    return render(request,'student/team_edit.html',{'content': instance, 'team_id':team_id, 'content_id':content_id})		
	
# Ajax 設為發表、取消發表
def team_make_publish(request):
    work_id = request.POST.get('workid')
    action = request.POST.get('action')
    if work_id and action :
        if action == 'set':            
            try :
                work = TeamContent.objects.get(id=work_id) 	
                work.publish = True
                work.save()
            except ObjectDoesNotExist :
                pass
        else : 
            try :
                work = TeamContent.objects.get(id=work_id) 				
                work.publish = False
                work.save()
            except ObjectDoesNotExist :
                pass             
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)


# 列出所有討論主題
class CourseListView(ListView):
    model = CourseWork
    context_object_name = 'courses'
    template_name = "student/course_list.html"		
    paginate_by = 20
    def get_queryset(self):        
        courseclasses = CourseClass.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("publication_date", "course_id")
        courses = []
        for courseclass in courseclasses:
            course = CourseWork.objects.get(id=courseclass.course_id)
            courses.append([course, courseclass])
        return courses
			
    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        context['classroom'] = classroom
        return context	

# 列出所有討論主題素材
class CourseContentListView(ListView):
    model = CourseContent
    context_object_name = 'contents'
    template_name = "student/course_content.html"		
    def get_queryset(self):
        contents = CourseContent.objects.filter(course_id=self.kwargs['course_id']).order_by("id")
        queryset = []
        for content in contents :
            exercises = CourseExercise.objects.filter(content_id=content.id)
            try :
                progress = CourseContentProgress.objects.get(student_id=self.request.user.id, content_id=content.id).progress
            except ObjectDoesNotExist:
                progress = 0
            pool = []
            #examclass_dict = dict(((examclass.exam_id, examclass) for examclass in ExamClass.objects.filter(classroom_id=self.kwargs['classroom_id'])))	
            finished = True
            for exercise in exercises: 
                append = False
                #註記
                if exercise.types == 0:            
                    sclasses = SpeculationClass.objects.filter(classroom_id=self.kwargs['classroom_id'])
                    s_ids = [s.forum_id for s in sclasses]
                    if exercise.exercise_id in s_ids:
                        append = True                            
                    #work = SpeculationClass.objects.get(classroom_id=self.kwargs['classroom_id'], forum_id=exercise.exercise_id)
                    sfworks = SSpeculationWork.objects.filter(student_id=self.request.user.id, index=exercise.exercise_id).order_by("-id")
                    if len(sfworks)> 0 :
                        works = [sfworks[0].publish, sfworks]
                        if not sfworks[0].publish:
                            finished = False
                    else :
                        finished = False
                        works = [False, sfworks]                                                    
                #測驗 
                elif exercise.types == 1:
                    questions = ExamQuestion.objects.filter(exam_id=exercise.exercise_id)
                    examclasses = ExamClass.objects.filter(classroom_id=self.kwargs['classroom_id'])
                    exam_ids = [exam.exam_id for exam in examclasses]
                    if exercise.exercise_id in exam_ids:
                        append = True
                    examwork_pool = ExamWork.objects.filter(student_id=self.request.user.id).order_by("-id")                    
                    #work = ExamClass.objects.get(classroom_id=self.kwargs['classroom_id'], exam_id=exercise.exercise_id)                    				
                    examworks = filter(lambda w: w.exam_id==exercise.exercise_id, examwork_pool)
                    retest = False
                    try :
                        examclass = ExamClass.objects.get(classroom_id=self.kwargs['classroom_id'], exam_id=exercise.exercise_id)
                    except ObjectDoesNotExist:
                        examclass = ExamClass(classroom_id=self.kwargs['classroom_id'], exam_id=exercise.exercise_id)
                    if len(examworks) < examclass.round_limit or examclass.round_limit == 0 :
                        retest = True
                    if len(examworks)> 0:
                        if not examworks[0].publish:
                            finished = False                            
                        if not retest :
                            works = [examworks[0].publish, exercise.exercise_id, examworks, len(questions), retest]
                        else :
                            works = [True, exercise.exercise_id, examworks, len(questions), retest]
                    else :  
                        finished = False
                        works = [False, exercise.exercise_id, 0, len(questions), retest]
                if append:                              
                    pool.append([exercise, works])
            queryset.append([content, pool, progress, finished])
        return queryset
			
    def get_context_data(self, **kwargs):
        context = super(CourseContentListView, self).get_context_data(**kwargs)
        coursework = CourseWork.objects.get(id=self.kwargs['course_id'])
        courseclasses = CourseClass.objects.filter(course_id=self.kwargs['course_id'])				
        context['coursework']= coursework
        context['course_id'] = self.kwargs['course_id']
        context['courseclasses'] = courseclasses
        context['classroom_id'] = self.kwargs['classroom_id']
        return context	
			
# Ajax 設為開啟素材
def course_progress(request):
    student_id = request.POST.get('studentid')
    content_id = request.POST.get('contentid')
    value = request.POST.get('progress')
    if student_id and content_id :
        try:
            progress = CourseContentProgress.objects.get(student_id=student_id, content_id=content_id)
            if value == "2":
                progress.finish_time = timezone.now()
            progress.progress = int(value)
            progress.save()
        except ObjectDoesNotExist :
            progress = CourseContentProgress(student_id=student_id, content_id=content_id, progress=1)
            progress.save()
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)


# 列出所有討論主題
class CourseStatusListView(ListView):
    model = Enroll
    context_object_name = 'enrolls'
    template_name = "student/course_status.html"		
    
    def get_queryset(self):
        enrolls = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("seat")
        student_ids = [enroll.student_id for enroll in enrolls]
        contents = CourseContent.objects.filter(course_id=self.kwargs['course_id'])
        content_ids = [content.id for content in contents]
        progress = CourseContentProgress.objects.filter(student_id__in=student_ids, content_id__in=content_ids)        
        queryset = []
        for enroll in enrolls:
            content_list = []
            for content in contents:
                status = list(filter(lambda w: w.student_id==enroll.student_id and w.content_id==content.id, progress))
                if len(status) > 0:
                    content_list.append(status[0])
                else:
                    content_list.append(CourseContentProgress(content_id=0))
            queryset.append([enroll, content_list])
        return queryset
			
    def get_context_data(self, **kwargs):
        context = super(CourseStatusListView, self).get_context_data(**kwargs)
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        context['classroom'] = classroom
        return context	

