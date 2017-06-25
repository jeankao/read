# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, CreateView
from student.models import Enroll, EnrollGroup, SWork, SFWork
from teacher.models import Classroom, TWork, FWork, FContent, FClass
from account.models import VisitorLog
from student.forms import EnrollForm, GroupForm, SeatForm, GroupSizeForm, SubmitForm, ForumSubmitForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
import re
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
import jieba

# 列出選修的班級
class ClassroomListView(ListView):
    model = Enroll
    context_object_name = 'enrolls'
    template_name = 'student/classroom.html'
    
    def get_queryset(self):
        queryset = []
        enrolls = Enroll.objects.filter(student_id=self.request.user.id).order_by("-id")
        for enroll in enrolls :
          classroom = Classroom.objects.get(id=enroll.classroom_id)
          queryset.append([enroll, classroom.teacher_id])
        return queryset          
    
# 查看可加入的班級
def classroom_add(request):
        classrooms = Classroom.objects.all().order_by('-id')
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
        enroll_group = []
        classroom_name=Classroom.objects.get(id=classroom_id).name
        for enroll in enrolls:
            login_times = len(VisitorLog.objects.filter(user_id=enroll.student_id))
            enroll_group.append([enroll, login_times])
        return render_to_response('student/classmate.html', {'classroom_name':classroom_name, 'enrolls':enroll_group}, context_instance=RequestContext(request))

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
        #classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        fclasses = FClass.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")
        forum_ids = []
        for fclass in fclasses:
            forum_ids.append(fclass.forum_id)
        queryset = FWork.objects.filter(id__in=forum_ids).order_by("-id")
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(ForumListView, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        return context	    

    # 限本班同學
    def render_to_response(self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(ForumListView, self).render_to_response(context)    
			
def forum_submit(request, classroom_id, index):
        scores = []
        works = SFWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
        contents = FContent.objects.filter(forum_id=index)
        fwork = FWork.objects.get(id=index)
        if request.method == 'POST':
            form = ForumSubmitForm(request.POST, request.FILES)
            if form.is_valid():						
                work = SFWork(index=index, student_id=request.user.id)		
                work.memo=form.cleaned_data['memo']
                work.publication_date = timezone.now()
                work.save()
                return redirect("/student/forum/memo/"+classroom_id+"/"+index)
            else:
                return render_to_response('student/forum_form.html', {'error':form.errors}, context_instance=RequestContext(request))
        else:
            if not works.exists():
                work = SFWork(index=0)
                form = ForumSubmitForm()
            else:
                work = works[0]
                form = ForumSubmitForm(instance=works[0])
        return render_to_response('student/forum_form.html', {'fwork':fwork, 'works':works, 'work':work, 'form':form, 'scores':scores, 'index':index, 'contents':contents}, context_instance=RequestContext(request))

def forum_show(request, index):
		work = []
		contents = FContent.objects.filter(forum_id=index).order_by("-id")
		try:
				works = SFWork.objects.filter(index=index, student_id=request.user.id).order_by("-id")
		except ObjectDoesNotExist:
				pass
		return render_to_response('student/forum_show.html', {'work':works[0], 'contents':contents}, context_instance=RequestContext(request))

 # 查詢某作業所有同學心得
def forum_memo(request, classroom_id, index):    
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    datas = []
    contents = FContent.objects.filter(forum_id=index).order_by("-id")
    teacher_id = Classroom.objects.get(id=classroom_id).teacher_id
    for enroll in enrolls:
        try:
            works = SFWork.objects.filter(index=index, student_id=enroll.student_id).order_by("id")
            datas.append([enroll, works])
        except ObjectDoesNotExist:
            works = [SFWork(index=0, publication_date=timezone.make_aware(datetime.datetime(2000, 1, 1, 0, 0)))]
            datas.append([enroll, works])
    def getKey(custom):
        if custom[1]:
            return custom[1][0].publication_date, -custom[0].seat
        else:
            return -custom[0].seat
    datas = sorted(datas, key=getKey, reverse=True)	
	
    return render_to_response('student/forum_memo.html', {'datas': datas, 'contents':contents, 'teacher_id':teacher_id}, context_instance=RequestContext(request))
	
def forum_history(request, user_id, index):
		work = []
		contents = FContent.objects.filter(forum_id=index).order_by("-id")
		try:
				works = SFWork.objects.filter(index=index, student_id=user_id).order_by("-id")
		except ObjectDoesNotExist:
				pass
		return render_to_response('student/forum_history.html', {'works':works, 'contents':contents}, context_instance=RequestContext(request))

def forum_like(request):
    forum_id = request.POST.get('forumid')  
    user_id = request.POST.get('userid')
    action = request.POST.get('action')
    likes = []
    sfworks = []
    if forum_id:
        try:
            sfworks = SFWork.objects.filter(index=forum_id, student_id=user_id).order_by("id")
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
                sfwork.save()
            else:
                if sfwork.likes:
                    likes = jsonDec.decode(sfwork.likes)
                    if request.user.id in likes:
                        likes.remove(request.user.id)
                        sfwork.likes = json.dumps(likes)
                        sfwork.save()
               
        except ObjectDoesNotExist:
            sfworks = []            
        
        return JsonResponse({'status':'ok', 'likes':sfworks[0].likes}, safe=False)
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
    teacher_id = Classroom.objects.get(id=classroom_id).teacher_id
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
    return render_to_response('student/forum_jieba.html', {'index': index, 'words':words, 'enrolls':enrolls, 'classroom':classroom}, context_instance=RequestContext(request))

# 查詢某班某詞句心得
def forum_word(request, classroom_id, index, word):
        enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
        work_ids = []
        datas = []
        pos = word.index('-')
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
		
