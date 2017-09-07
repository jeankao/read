# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.db.models import *
from forms import LoginForm, UserRegistrationForm, PasswordForm, RealnameForm, LineForm, SchoolForm, EmailForm, DomainForm, LevelForm, SiteImageForm, UploadFileForm
from django.contrib.auth.models import User
from account.models import Profile, PointHistory, Log, Message, MessageContent, MessagePoll, Visitor, VisitorLog, Domain, Level, Site, Parent, ImportUser
from student.models import Enroll, SFWork, SSpeculationWork
from teacher.models import Classroom, Assistant, FWork, FClass, SpeculationWork, SpeculationClass
from django.core.exceptions import ObjectDoesNotExist
#from account.templatetags import tag 
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.models import Group
from django.http import JsonResponse
import sys, os
from django.http import HttpResponse
from mimetypes import MimeTypes
import StringIO
import xlsxwriter
import datetime
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import datetime
from django.apps import apps
import json
import urllib
from django.db.models import Q
from itertools import groupby
from collections import OrderedDict
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from django.forms.models import model_to_dict
from django.conf import settings
from wsgiref.util import FileWrapper
from django.http import HttpResponse
#from helper import VideoLogHelper
import django_excel as excel

# 判斷是否開啟事件記錄
def is_event_open(request):
        return True
        
# 判斷是否為任教學生
def is_student(user_id, request):
    classrooms = Classroom.objects.filter(teacher_id=request.user.id)
    for classroom in classrooms:
        if Enroll.objects.filter(classroom_id=classroom.id, student_id=user_id).exists(): 
            return True
    return False
    
# 判斷是否為本班同學
def is_classmate(user_id, classroom_id):
    return Enroll.objects.filter(student_id=user_id, classroom_id=classroom_id).exists()

# 網站首頁
def homepage(request):
    models = apps.get_models()
    row_count = 0
    for model in models:
        row_count = row_count + model.objects.count()
    users = User.objects.all()
    try :
        site = Site.objects.get(id=1)
        site.home_count = site.home_count + 1
        site.save()
    except ObjectDoesNotExist:
        #網站資訊
        site = Site(site_name='南港高中', site_image='images/home.jpg')
        site.save()
    classroom_count = Classroom.objects.all().count()
    teacher_count = Group.objects.get(name="teacher").user_set.count()
    forum_count = FWork.objects.all().count()
    speculation_count = SpeculationWork.objects.all().count()		
    return render_to_response('homepage.html', {'forum_count':forum_count, 'speculation_count':speculation_count, 'teacher_count':teacher_count, 'classroom_count':classroom_count, 'row_count':row_count, 'user_count':len(users), 'site': site}, context_instance=RequestContext(request))

# 作者
def developer(request):
    return render_to_response('developer.html', context_instance=RequestContext(request))

	
	
# 使用者登入功能
def user_login(request):
        message = None
        test = ""
        if request.method == "POST":
                form = LoginForm(request.POST)
                if form.is_valid():
                        username = request.POST['username']
                        password = request.POST['password']
                        user = authenticate(username=username, password=password)
                        if user is not None:
                                if user.is_active:
                                        if user.id == 1:
                                            if user.first_name == "": 
                                                user.first_name = "管理員"
                                                user.save()
                                                # create Message
                                                title = "請修改您的姓名"
                                                url = "/account/realname"
                                                message = Message.create(title=title, url=url, time=timezone.now())
                                                message.save()      
                                                # message for group member
                                                messagepoll = MessagePoll.create(message_id = message.id,reader_id=1)
                                                messagepoll.save()                                                             
                                                # 學習領域
                                                domains = ['國語文','英語文','數學','社會','自然','科技','藝術', '綜合','健體']
                                                for domain_name in domains:
                                                    domain = Domain(title=domain_name)
                                                    domain.save()
                                                levels = ['國七','國八','國九']
                                                for level_name in levels:
                                                    level = Level(title=level_name)
                                                    level.save()	
                                                
                                        # 登入成功，導到大廳
                                        login(request, user)
                                        # 記錄系統事件
                                        log = Log(user_id=request.user.id, event='登入系統')
                                        log.save()
                                        # 記錄訪客資訊
                                        try:
                                            site = Site.objects.get(id=1)
                                        except ObjectDoesNotExist:
                                            #網站資訊
                                            site = Site(site_name='南港高中', site_image='images/home.jpg')
                                            site.save()
                                        site.visitor_count = site.visitor_count + 1
                                        site.save()
                                        
                                        year = localtime(timezone.now()).year
                                        month =  localtime(timezone.now()).month
                                        day =  localtime(timezone.now()).day
                                        date_number = year * 10000 + month*100 + day
                                        try:
                                            visitor = Visitor.objects.get(date=date_number)
                                        except ObjectDoesNotExist:
                                            visitor = Visitor(date=date_number)
                                        visitor.count = visitor.count + 1
                                        visitor.save()
                                        
                                        visitorlog = VisitorLog(visitor_id=visitor.id, user_id=user.id, IP=request.META.get('REMOTE_ADDR'))
                                        visitorlog.save()
                                        
                                        return redirect('/account/dashboard/0')
                                else:
                                        message = "Your user is inactive"
                        else:
                            # 記錄系統事件
                            if is_event_open(request) :                            
                                log = Log(user_id=0, event='登入失敗')
                                log.save()                                
                            message = "無效的帳號或密碼!"
        else:
                form = LoginForm()
        return render_to_response('registration/login.html', {'test': test, 'message': message, 'form': form}, context_instance=RequestContext(request))

# 記錄登出
def suss_logout(request, user_id):
    # 記錄系統事件
    if is_event_open(request) :    
        log = Log(user_id=user_id, event='登出系統')
        log.save()    
    return redirect('/account/login/')

# 訊息
class MessageListView(ListView):
    context_object_name = 'messages'
    paginate_by = 20
    template_name = 'account/dashboard.html'

    def get_queryset(self):             
        query = []
        #公告
        if self.kwargs['action'] == "1":
            messagepolls = MessagePoll.objects.filter(reader_id=self.request.user.id, message_type=1).order_by('-message_id')
        #私訊
        elif self.kwargs['action'] == "2":
            messagepolls = MessagePoll.objects.filter(reader_id=self.request.user.id, message_type=2).order_by('-message_id')
        #系統
        elif self.kwargs['action'] == "3":
            messagepolls = MessagePoll.objects.filter(reader_id=self.request.user.id, message_type=3).order_by('-message_id')						
        else :
            messagepolls = MessagePoll.objects.filter(reader_id=self.request.user.id).order_by('-message_id')
        for messagepoll in messagepolls:
            query.append([messagepoll, messagepoll.message])
        return query
        
    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        context['action'] = self.kwargs['action']
        return context
# 註冊帳號                  
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password                 
            new_user.set_password(
                form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            profile = Profile(user=new_user)
            profile.save()
            # 記錄系統事件
            if is_event_open(request) :   
                log = Log(user_id=new_user.id, event='註冊帳號成功')
                log.save()                
        
            # create Message
            title = "請洽詢任課教師課程名稱及選課密碼"
            url = "/student/classroom/add"
            message = Message.create(title=title, url=url, time=timezone.now())
            message.save()                        
                    
            # message for group member
            messagepoll = MessagePoll.create(message_id = message.id,reader_id=new_user.id)
            messagepoll.save()               
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'form': form})
      
# 顯示個人檔案
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    enrolls = Enroll.objects.filter(student_id=user_id)
    try: 
        profile = Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        profile = Profile(user=user)
        profile.save()

    # 計算積分    
    credit = profile.work + profile.like + profile.reply
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=request.user.id, event='查看個人檔案')
        log.save()        
        
    #檢查是否為教師或同班同學
    user_enrolls = Enroll.objects.filter(student_id=request.user.id)
    for enroll in user_enrolls:
        if is_classmate(user_id, enroll.classroom_id) or request.user.id == 1:
          return render_to_response('account/profile.html',{'enrolls':enrolls, 'profile': profile,'user_id':int(user_id), 'credit':credit}, context_instance=RequestContext(request))	
    if int(user_id) == request.user.id:	
        return render_to_response('account/profile.html',{'enrolls':enrolls, 'profile': profile,'user_id':int(user_id), 'credit':credit}, context_instance=RequestContext(request))	
    return redirect("/")

	# 修改密碼
def password(request, user_id):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.set_password(request.POST['password'])
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改<'+user.first_name+u'>密碼成功')
                log.save()                
            return redirect('homepage')
    else:
        canEdit = False
        if request.user.id == int(user_id):
            canEdit = True
        else :
            enrolls = Enroll.objects.filter(student_id=user_id)
            for enroll in enrolls:
                classroom = Classroom.objects.get(id=enroll.classroom_id)
                if request.user.id == classroom.teacher_id:
                    canEdit = True
                assistants = Assistant.objects.filter(user_id=request.user.id)
                for assistant in assistants:
                    if assistant.classroom_id == enroll.classroom_id:
                        canEdit = True
            if request.user.id == 1:
                canEdit = True
        if canEdit:
            form = PasswordForm()
            user = User.objects.get(id=user_id)
        else :
            return redirect('homepage')
    return render_to_response('account/password.html',{'form': form, 'user':user}, context_instance=RequestContext(request))

# 修改他人的真實姓名
def adminrealname(request, user_id):
    if request.method == 'POST':
        form = RealnameForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.first_name =form.cleaned_data['first_name']
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改姓名<'+user.first_name+'>')
                log.save()                
            return redirect('/account/userlist/')
    else:
        teacher = False
        enrolls = Enroll.objects.filter(student_id=user_id)
        for enroll in enrolls:
            classroom = Classroom.objects.get(id=enroll.classroom_id)
            if request.user.id == classroom.teacher_id:
                teacher = True
                break
        if teacher or request.user.id == 1:
            user = User.objects.get(id=user_id)
            form = RealnameForm(instance=user)
        else:
            return redirect("/")

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))
	
# 修改自己的真實姓名
def realname(request):
    if request.method == 'POST':
        form = RealnameForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.first_name =form.cleaned_data['first_name']
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改姓名<'+user.first_name+'>')
                log.save()                
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = RealnameForm(instance=user)

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))

# 修改學校名稱
def adminschool(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.last_name =form.cleaned_data['last_name']
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改學校名稱<'+user.last_name+'>')
                log.save()                
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = SchoolForm(instance=user)

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))
    
# 修改信箱
def adminemail(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.email =form.cleaned_data['email']
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改信箱<'+user.first_name+'>')
                log.save()                
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = EmailForm(instance=user)

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))    

# 記錄積分項目
class LogListView(ListView):
    context_object_name = 'logs'
    paginate_by = 20
    template_name = 'account/log_list.html'
	
    def get_queryset(self):
        # 記錄系統事件
        if self.kwargs['kind'] == "1" :
            log = Log(user_id=self.kwargs['user_id'], event='查看積分--討論區')
        elif  self.kwargs['kind'] == "2" :
            log = Log(user_id=self.kwargs['user_id'], event='查看積分--按讚')      
        elif  self.kwargs['kind'] == "3" :
            log = Log(user_id=self.kwargs['user_id'], event='查看積分--留言')            
        elif  self.kwargs['kind'] == "4" :
            log = Log(user_id=self.kwargs['user_id'], event='查看積分--思辨區')
        else :
            log = Log(user_id=self.kwargs['user_id'], event='查看全部積分')                        
        if is_event_open(self.request) :               
            log.save()                
        if not self.kwargs['kind'] == "0" :
            queryset = PointHistory.objects.filter(user_id=self.kwargs['user_id'],kind=self.kwargs['kind']).order_by('-id')
        else :
            queryset = PointHistory.objects.filter(user_id=self.kwargs['user_id']).order_by('-id')		
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LogListView, self).get_context_data(**kwargs)
        user_name = User.objects.get(id=self.kwargs['user_id']).first_name
        context.update({'user_name': user_name})
        return context		
        
# 超級管理員可以查看所有帳號
class UserListView(ListView):
    context_object_name = 'users'
    paginate_by = 20
    template_name = 'account/user_list.html'
    
    def get_queryset(self):
        # 記錄系統事件
        if is_event_open(self.request) :           
            log = Log(user_id=1, event='管理員查看帳號')
            log.save()         
        if self.request.GET.get('account') != None:
            keyword = self.request.GET.get('account')
            queryset = User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword)).order_by('-id')
        else :
            queryset = User.objects.all().order_by('-id')				
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        account = self.request.GET.get('account')
        context.update({'account': account})
        return context	
    
# Ajax 設為教師、取消教師
def make(request):
    user_id = request.POST.get('userid')
    action = request.POST.get('action')
    if user_id and action :
        user = User.objects.get(id=user_id)           
        try :
            group = Group.objects.get(name="teacher")	
        except ObjectDoesNotExist :
            group = Group(name="teacher")
            group.save()
        if action == 'set':            
            # 記錄系統事件
            log = Log(user_id=1, event=u'管理員設為教師<'+user.first_name+'>')
            log.save()                        
            group.user_set.add(user)
            # create Message
            title = "<" + request.user.first_name + u">設您為教師"
            url = "/teacher/classroom"
            message = Message.create(title=title, url=url, time=timezone.now())
            message.save()                        
                    
            # message for group member
            messagepoll = MessagePoll.create(message_id = message.id,reader_id=user_id)
            messagepoll.save()    
        else : 
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=1, event=u'取消教師<'+user.first_name+'>')
                log.save()              
            group.user_set.remove(user)  
            # create Message
            title = "<"+ request.user.first_name + u">取消您為教師"
            url = "/"
            message = Message.create(title=title, url=url, time=timezone.now())
            message.save()                        
                    
            # message for group member
            messagepoll = MessagePoll.create(message_id = message.id,reader_id=user_id)
            messagepoll.save()               
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':user.first_name}, safe=False)        

def message(request, messagepoll_id):
    messagepoll = MessagePoll.objects.get(id=messagepoll_id)
    messagepoll.read = True
    messagepoll.save()
    message = Message.objects.get(id=messagepoll.message_id)
    return redirect(message.url)
    
# 列出所有私訊
class LineListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'account/line_list.html'    
    paginate_by = 20
    
    def get_queryset(self):
        # 記錄系統事件
        if is_event_open(self.request) :    
            log = Log(user_id=self.request.user.id, event='查看所有私訊')
            log.save()        
        queryset = Message.objects.filter(author_id=self.request.user.id).order_by("-id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LineListView, self).get_context_data(**kwargs)
        return context	 
        
# 列出同學以私訊
class LineClassListView(ListView):
    model = Enroll
    context_object_name = 'enrolls'
    template_name = 'account/line_class.html'   
    
    def get_queryset(self):
        # 記錄系統事件
        if is_event_open(self.request) :    
            log = Log(user_id=self.request.user.id, event='列出同學以私訊')
            log.save()        
        queryset = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("seat")
        return queryset
        
    # 限本班同學
    def render_to_response(self, context):
        if not is_classmate(self.request.user.id, self.kwargs['classroom_id']):
            return redirect('/')
        return super(LineClassListView, self).render_to_response(context)            
                
#新增一個私訊
class LineCreateView(CreateView):
    model = Message
    context_object_name = 'messages'    
    form_class = LineForm
    template_name = 'account/line_form.html'     

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user_name = User.objects.get(id=self.request.user.id).first_name
        self.object.title = u"[私訊]" + user_name + ":" + self.object.title
        self.object.author_id = self.request.user.id
        self.object.reader_id = self.kwargs['user_id']
        self.object.type = 2
        self.object.save()
        self.object.url = "/account/line/detail/" + self.kwargs['classroom_id'] + "/" + str(self.object.id)
        self.object.classroom_id = 0 - int(self.kwargs['classroom_id'])
        self.object.save()
        if self.request.FILES:
            for file in self.request.FILES.getlist('files'):
                content = MessageContent()
                fs = FileSystemStorage()
                filename = uuid4().hex
                content.title = file.name
                content.message_id = self.object.id
                content.filename = str(self.request.user.id)+"/"+filename
                fs.save("static/upload/"+str(self.request.user.id)+"/"+filename, file)
                content.save()
        # 訊息
        messagepoll = MessagePoll(message_id=self.object.id, reader_id=self.kwargs['user_id'], message_type=2, classroom_id=0-int(self.kwargs['classroom_id']))
        messagepoll.save()
        # 記錄系統事件
        if is_event_open(self.request) :            
            log = Log(user_id=self.request.user.id, event=u'新增私訊<'+self.object.title+'>')
            log.save()                
        return redirect("/account/line/")      
        
    def get_context_data(self, **kwargs):
        context = super(LineCreateView, self).get_context_data(**kwargs)
        context['user_id'] = self.kwargs['user_id']
        context['classroom_id'] = self.kwargs['classroom_id']
        messagepolls = MessagePoll.objects.filter(reader_id=self.kwargs['user_id'],  classroom_id=0 - int(self.kwargs['classroom_id'])).order_by('-id')
        messages = []
        for messagepoll in messagepolls:
            message = Message.objects.get(id=messagepoll.message_id)
            if message.author_id == self.request.user.id :
                messages.append([message, messagepoll.read])
        context['messages'] = messages
        return context	 
        
# 查看私訊內容
def line_detail(request, classroom_id, message_id):
    message = Message.objects.get(id=message_id)
    files = MessageContent.objects.filter(message_id=message_id)
    messes = Message.objects.filter(author_id=message.author_id, reader_id=request.user.id).order_by("-id")
    try:
        messagepoll = MessagePoll.objects.get(message_id=message_id, reader_id=request.user.id)
        messagepoll.read = True
        messagepoll.save()
    except :
        messagepoll = MessagePoll()
    return render_to_response('account/line_detail.html', {'files':files, 'lists':messes, 'classroom_id':classroom_id, 'message':message, 'messagepoll':messagepoll}, context_instance=RequestContext(request))

# 下載檔案
def line_download(request, file_id):
    content = MessageContent.objects.get(id=file_id)
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
def line_showpic(request, file_id):
        content = MessageContent.objects.get(id=file_id)
        return render_to_response('student/forum_showpic.html', {'content':content}, context_instance=RequestContext(request))

	
	
# 列出所有日期訪客
class VisitorListView(ListView):
    model = Visitor
    context_object_name = 'visitors'
    template_name = 'account/visitor_list.html'    
    paginate_by = 20
    
    def get_queryset(self):
        # 記錄系統事件
        if is_event_open(self.request) :
            if not self.request.user.is_authenticated():
                user_id = 0
            else :
                user_id = self.request.user.id
            log = Log(user_id=user_id, event='查看所有訪客')
            log.save()        
        visitors = Visitor.objects.all().order_by('-id')
        queryset = []
        for visitor in visitors:
            queryset.append([int(str(visitor.date)[0:4]), int(str(visitor.date)[4:6]),int(str(visitor.date)[6:8]),visitor])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(VisitorListView, self).get_context_data(**kwargs)
        first_element = Visitor.objects.all().order_by("-id")[0]
        end_year = int(str(first_element.date)[0:4])
        last_element = Visitor.objects.all().order_by("id")[0]
        start_year = int(str(last_element.date)[0:4])
        context['height'] = 200+ (end_year-start_year)*200
        visitors = Visitor.objects.all().order_by('id')
        queryset = []
        for visitor in visitors:
            queryset.append([int(str(visitor.date)[0:4]), int(str(visitor.date)[4:6]),int(str(visitor.date)[6:8]),visitor])
        context['total_visitors'] = queryset
        return context	
			
# 列出單日日期訪客
class VisitorLogListView(ListView):
    model = VisitorLog
    context_object_name = 'visitorlogs'
    template_name = 'account/visitorlog_list.html'    
    paginate_by = 50
    
    def get_queryset(self):
        # 記錄系統事件
        visitor = Visitor.objects.get(id=self.kwargs['visitor_id'])
        if is_event_open(self.request) :    
            log = Log(user_id=self.request.user.id, event='查看單日訪客<'+str(visitor.date)+'>')
            log.save()        
        queryset = VisitorLog.objects.filter(visitor_id=self.kwargs['visitor_id']).order_by('-id')
        return queryset
        
    def render_to_response(self, context):
        if not self.request.user.is_authenticated():
            return redirect('/')
        return super(VisitorLogListView, self).render_to_response(context)

# 下載檔案
def download(request, filename):
    #down_file = File.objects.get(name = filename)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DOWNLOAD_URL = BASE_DIR+"/download/"
    file_path = DOWNLOAD_URL + filename
    file_name = filename
    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    mime = MimeTypes()
    type, encoding = mime.guess_type(file_name)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        filename_header = 'filename=%s' % file_name.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        filename_header = ''
    else:
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(file_name.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=request.user.id, event=u'下載檔案<'+filename+'>')
        log.save()     
    return response

def avatar(request):
    profile = Profile.objects.get(user = request.user)
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=request.user.id, event=u'查看個人圖像')
        log.save()        
    return render_to_response('account/avatar.html', {'avatar':profile.avatar}, context_instance=RequestContext(request))
    
# 記錄系統事件
class EventListView(ListView):
    context_object_name = 'events'
    paginate_by = 50
    template_name = 'account/event_list.html'

    def get_queryset(self):    
        user = User.objects.get(id=self.kwargs['user_id'])
        # 記錄系統事件
        if is_event_open(self.request) :           
            log = Log(user_id=self.request.user.id, event=u'查看個人事件<'+user.first_name+'>')
            log.save()       
        if self.request.GET.get('q') != None:
            queryset = Log.objects.filter(user_id=self.kwargs['user_id'], event__icontains=self.request.GET.get('q')).order_by('-id')
        else :
            queryset = Log.objects.filter(user_id=self.kwargs['user_id']).order_by('-id')
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        context.update({'q': q})
        return context	
        
    # 限本人 
    def render_to_response(self, context):
        #if is_teacher(self.kwargs['user_id'], self.request) :
        #    return redirect('/')
        return super(EventListView, self).render_to_response(context)      
			
# 記錄系統事件
class EventAdminListView(ListView):
    context_object_name = 'events'
    paginate_by = 50	
    template_name = 'account/event_admin_list.html'

    def get_queryset(self):    
        # 記錄系統事件
        log = Log(user_id=1, event=u'管理員查看系統事件')
        log.save()       
        if self.request.GET.get('q') != None:
            queryset = Log.objects.filter(event__icontains=self.request.GET.get('q')).order_by('-id')
        else :
            queryset = Log.objects.all().order_by('-id')					
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(EventAdminListView, self).get_context_data(**kwargs)
        classrooms = Classroom.objects.all().order_by('-id')
        context['classrooms'] = classrooms
        q = self.request.GET.get('q')
        context.update({'q': q})
        return context	
        
    # 限管理員
    def render_to_response(self, context):
        if not self.request.user.id == 1 :
            return redirect('/')
        return super(EventAdminListView, self).render_to_response(context)      
        
# 記錄系統事件
class EventAdminClassroomListView(ListView):
    context_object_name = 'events'
    paginate_by = 50
    template_name = 'account/event_admin_classroom_list.html'

    def get_queryset(self):    
        # 記錄系統事件
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        log = Log(user_id=1, event=u'管理員查看班級事件<'+classroom.name+'>')
        log.save()
        if self.request.GET.get('q') != None:
            queryset = Log.objects.filter(classroom_id=self.kwargs['classroom_id'], event__icontains=self.request.GET.get('q')).order_by('-id')
        else :
            queryset = Log.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by('-id')
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(EventAdminClassroomListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        context.update({'q': q})
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        context['classroom'] = classroom        
        return context	
        
    # 限管理員
    def render_to_response(self, context):
        if not self.request.user.id == 1:
            return redirect('/')
        return super(EventAdminClassroomListView, self).render_to_response(context)     
from django.utils.dateparse import parse_date
# 記錄系統事件
class EventCalendarView(ListView):
    context_object_name = 'events'
    #paginate_by = 50
    template_name = 'account/event_calendar.html'

    def get_queryset(self):    
        # 記錄系統事件
        user = User.objects.get(id=self.kwargs['user_id'])
        log = Log(user_id=self.request.user.id, event=u'查看登入記錄<'+user.first_name+'>')
        log.save()
        user_logs = Log.objects.filter(user_id=user.id, event="登入系統").extra({'logdate': "to_char(publish, 'YYYY-MM-DD')"}).values('logdate').annotate(count=Count('id')).order_by('logdate')
        return user_logs
        
    def get_context_data(self, **kwargs):
        context = super(EventCalendarView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['user_id'])
        context['user1'] = user
        return context	 

# 記錄系統事件
class EventTimeLineView(ListView):
    context_object_name = 'events'
    #paginate_by = 50
    template_name = 'account/event_timeline.html'

    def get_queryset(self):    
        # 記錄系統事件
        user = User.objects.get(id=self.kwargs['user_id'])
        log = Log(user_id=self.request.user.id, event=u'查看使用記錄<'+user.first_name+'>')
        log.save()
        #user_logs = Log.objects.filter(user_id=user.id, event="登入系統").extra({'logdate': "to_char(publish, 'YYYY-MM-DD')"}).values('logdate').annotate(count=Count('id')).order_by('logdate')
        user_logs = Log.objects.filter(user_id=user.id).order_by("id")
        logs = groupby(user_logs, key=lambda row: (localtime(row.publish).year, localtime(row.publish).month, localtime(row.publish).day, localtime(row.publish).hour))
        week = OrderedDict()
        month_list = []
        for key, value in logs:           
            month_list = [[key, list(value)]]
            week_number = key[0]*1000 + datetime(*key).isocalendar()[1]
            if week.has_key(week_number):
                pass
                week[week_number].append(month_list)
            else:
                week[week_number] = [month_list]
        #sorted(week.iteritems())
        return sorted(week.iteritems())
        
    def get_context_data(self, **kwargs):
        context = super(EventTimeLineView, self).get_context_data(**kwargs)
        context['week_number'] = datetime(*(2017,1,30)).isocalendar()[1]
        user = User.objects.get(id=self.kwargs['user_id'])
        context['user1'] = user
        user = User.objects.get(id=self.kwargs['user_id'])	
        user_logs = Log.objects.filter(user_id=user.id).order_by("-id")
        logs = groupby(user_logs, key=lambda row: (localtime(row.publish).year, localtime(row.publish).month, localtime(row.publish).day))
        week = OrderedDict()
        for key, value in logs:        
            week_number = key[0]*1000 + datetime(*key).isocalendar()[1]	
            if week.has_key(week_number):
                week[week_number] += 1
            else:
                week[week_number] = 1
        sorted(week.iteritems())
        day = []    
        for key in week:
            day.append(week[key])
        context['day_count'] = day
        return context
			
# 記錄系統事件
class EventTimeLogView(ListView):
    context_object_name = 'events'
    paginate_by = 50
    template_name = 'account/event_timelog.html'

    def get_queryset(self):    
        # 記錄系統事件
        user = User.objects.get(id=self.kwargs['user_id'])
        date_string = self.kwargs['hour']
        year = int(date_string[0:4])
        month = int(date_string[4:6])
        day = int(date_string[6:8])
        hour = int(date_string[8:10])
        log = Log(user_id=self.request.user.id, event=u'查看分時使用記錄<'+user.first_name+'>')
        log.save()
        user_logs = Log.objects.filter(user_id=user.id, publish__year=year, publish__month=month, publish__day=day, publish__hour=hour).order_by("-id")
        return user_logs
        
    def get_context_data(self, **kwargs):
        context = super(EventTimeLogView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['user_id'])
        context['user1'] = user
        date_string = self.kwargs['hour']
        year = date_string[0:4]
        month = date_string[4:6]
        day = date_string[6:8]
        hour = date_string[8:10]
        context['hour'] = [year, month, day, hour]
        return context
			
# 記錄系統事件
class EventVideoView(ListView):
    context_object_name = 'events'
    #paginate_by = 50
    template_name = 'account/event_video.html'

    def get_queryset(self):    
				# 記錄系統事件
				classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
				log = Log(user_id=self.request.user.id, event=u'查看影片觀看記錄<'+classroom.name+'>')
				log.save()

				enrolls = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id'], seat__gt=0).order_by("seat")
				events = []
				for student in enrolls: 
						videos = VideoLogHelper().getLogByUserid(student.student_id)
						length = 0
						for video in videos: 
								for log in videos[video]:									
										length += log['length']
						events.append([student, length/60])
				return events
        
    def get_context_data(self, **kwargs):
        context = super(EventVideoView, self).get_context_data(**kwargs)
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        context['classroom'] = classroom
        enrolls = Enroll.objects.filter(classroom_id=classroom.id)
        context['height'] = 100 + enrolls.count() * 40
        return context
			
    # 限本班同學
    def render_to_response(self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(EventVideoView, self).render_to_response(context)        
	
			

# 新增教學筆記
def note_add(request):
    classroom_id = request.POST.get('classroomid')
    lesson = request.POST.get('lesson')
    memo = request.POST.get('memo')
    user_id = request.POST.get('userid')
    note_id = request.POST.get('noteid')
    if note_id == 0 or note_id == "0" :
        note = Note(classroom_id=classroom_id, user_id=user_id, lesson=lesson, memo=memo)
        note.save()	
        if is_event_open(request) :       
            log = Log(user_id=request.user.id, event=u'新增教學筆記')
            log.save()        
    else : 
        try: 
            note = Note.objects.get(id=note_id)
            note.memo = memo
            note.save()
            if is_event_open(request) :       
                log = Log(user_id=request.user.id, event=u'編輯教學筆記')
                log.save()    
        except:
            pass
    return JsonResponse({'status':'ok', 'note_id':note_id}, safe=False)

# 新增教學筆記
def note_get(request):
    classroom_id = request.POST.get('classroomid')
    lesson = request.POST.get('lesson')
    user_id = request.POST.get('userid')
    note_text = ""
    if not classroom_id == "0" :
        classroom_name = Classroom.objects.get(id=classroom_id).name
    else :
        classroom_name = "MyNote"
    notes = Note.objects.filter(classroom_id=classroom_id, user_id=user_id, lesson=lesson).order_by('-id')
    if notes.exists():
        for note in notes:
            note_text = note_text + str(localtime(note.publication_date).strftime("%Y-%m-%d %H:%M:%S"))
            note_text = note_text + " <a href=javascript:note_add('" + classroom_name + "'," + str(classroom_id) + ",'" + str(lesson) + "'," + str(note.id) + u")><img src='/static/images/icon_edit.png'>編輯筆記</a>" 
            note_text = note_text + "<div class=note_content_" + str(note.id) + ">" + note.memo + "</div>"
        return JsonResponse({'status':'ok', 'note_text':note_text, 'classroom_id':classroom_id}, safe=False)
    else :
        notes = None
        return JsonResponse({'status':'no_ok', 'note_text':note_text}, safe=False)
          
# 影片記錄
def videolog(request):
		tabName = request.POST.get('tabName')
		lesson = request.POST.get('lesson')
		duration = video_duration[video_url[lesson, tabName.encode('UTF-8')]]
		xlist = VideoLogHelper().getLogByUserid_Lesson_Tab(request.user.id, lesson, tabName)
		return JsonResponse({'status':'ok', 'duration':duration, 'recs':json.dumps(xlist)}, safe=False)
     
# 管理介面 
def admin(request):
    return render_to_response('account/admin.html', context_instance=RequestContext(request))
	
# 學習領域
class DomainListView(ListView):
    context_object_name = 'domains'
    template_name = 'account/domain.html'

    def get_queryset(self):    
        # 記錄系統事件
        log = Log(user_id=1, event=u'管理員查看學習領域')
        log.save()       
        queryset = Domain.objects.all().order_by('-id')					
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(DomainListView, self).get_context_data(**kwargs)
        return context	

class DomainCreateView(CreateView):
    template_name = 'form.html'	
    model = Domain
    fields = ['title']
    success_url = '/account/admin/domain/'

class DomainUpdateView(UpdateView):
    model = Domain
    fields = ['title']
    template_name = 'form.html'
    success_url = '/account/admin/domain/'		
		     
# 年級
class LevelListView(ListView):
    context_object_name = 'levels'
    template_name = 'account/level.html'

    def get_queryset(self):    
        # 記錄系統事件
        log = Log(user_id=1, event=u'管理員查看年級')
        log.save()       
        queryset = Level.objects.all().order_by('-id')					
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(LevelListView, self).get_context_data(**kwargs)
        return context	

class LevelCreateView(CreateView):
    template_name = 'form.html'	
    model = Level
    fields = ['title']
    success_url = '/account/admin/level/'

class LevelUpdateView(UpdateView):
    model = Level
    fields = ['title']
    template_name = 'form.html'
    success_url = '/account/admin/level/'		
		     
class SitenameUpdateView(UpdateView):
    model = Site
    fields = ['site_name']
    template_name = 'form.html'
    success_url = '/account/admin/'		

# 上傳首頁圖片
def siteimage(request):
        if request.method == 'POST':
            form = SiteImageForm(request.POST)			
            if form.is_valid() and request.FILES:
                myfile =  request.FILES.get("file", "")
                fs = FileSystemStorage()
                filename = uuid4().hex
                fs.save("static/upload/"+str(request.user.id)+"/"+filename, myfile)
                site = Site.objects.get(id=1)
                site.site_image='upload/1/'+filename
                site.save()
                return redirect("/")
            else:
      	        return render_to_response('account/siteimage_form.html', {'errors':form}, context_instance=RequestContext(request))
        else:
            form = SiteImageForm()
        return render_to_response('account/siteimage_form.html', {'form':form}, context_instance=RequestContext(request))

# 討論區作業
class ForumListView(ListView):
    context_object_name = 'forums'
    template_name = 'account/forum_list.html'
    paginate_by = 10
		
    def get_queryset(self):    
        # 記錄系統事件
        log = Log(user_id=1, event=u'查看個人討論區作業')
        log.save()       
        classroom_ids = Enroll.objects.filter(student_id=self.kwargs['user_id'], seat__gt=0).values_list('classroom_id')				
        forum_dict = dict(((fwork.id, fwork) for fwork in FWork.objects.all()))
        fclasses = FClass.objects.filter(classroom_id__in=classroom_ids).order_by("-publication_date")
        forum_ids = []
        for fclass in fclasses:
            forum_ids.append(fclass.forum_id)
        queryset = []
        sfwork_pool = SFWork.objects.filter(student_id=self.kwargs['user_id']).order_by("id")
        for fclass in fclasses:
            sfworks = filter(lambda w: w.index==fclass.forum_id, sfwork_pool)
            if len(sfworks) > 0 :
                 queryset.append([fclass, forum_dict[fclass.forum_id], sfworks[0].publish, len(sfworks)])
            else :
                 queryset.append([fclass, forum_dict[fclass.forum_id], False, 0])
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(ForumListView, self).get_context_data(**kwargs)
        context['user_id']= self.kwargs['user_id']
        return context	

# 思辨區作業
class SpeculationListView(ListView):
    context_object_name = 'forums'
    template_name = 'account/speculation_list.html'
    paginate_by = 10
		
    def get_queryset(self):    
        # 記錄系統事件
        log = Log(user_id=1, event=u'查看個人思辨區作業')
        log.save()       
        classroom_ids = Enroll.objects.filter(student_id=self.kwargs['user_id'], seat__gt=0).values_list('classroom_id')				
        forum_dict = dict(((fwork.id, fwork) for fwork in SpeculationWork.objects.all()))
        fclasses = SpeculationClass.objects.filter(classroom_id__in=classroom_ids).order_by("-publication_date")
        forum_ids = []
        for fclass in fclasses:
            forum_ids.append(fclass.forum_id)
        queryset = []
        sfwork_pool = SSpeculationWork.objects.filter(student_id=self.kwargs['user_id']).order_by("-id")
        for fclass in fclasses:
            sfworks = filter(lambda w: w.index==fclass.forum_id, sfwork_pool)
            if len(sfworks) > 0 :
                 queryset.append([fclass, forum_dict[fclass.forum_id], sfworks[0].publish, len(sfworks)])
            else :
                 queryset.append([fclass, forum_dict[fclass.forum_id], False, 0])
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(SpeculationListView, self).get_context_data(**kwargs)
        context['user_id']= self.kwargs['user_id']
        return context	
			
# 家長
class ParentListView(ListView):
    context_object_name = 'users'
    template_name = 'account/parent_list.html'
		
    def get_queryset(self):    
        # 記錄系統事件
        log = Log(user_id=1, event=u'查看家長設定')
        log.save()       
        queryset= Parent.objects.filter(student_id=self.request.user.id)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(ParentListView, self).get_context_data(**kwargs)
        return context	
			
# 家長
class ParentSearchListView(ListView):
    context_object_name = 'users'
    template_name = 'account/parent_search.html'
		
    def get_queryset(self):    
        # 記錄系統事件
        log = Log(user_id=self.request.user.id, event=u'搜尋家長帳號')
        log.save()
        queryset = []
        if self.request.GET.get('word') != None:
            keyword = self.request.GET.get('word')
            queryset = User.objects.filter(Q(username=keyword) | Q(first_name=keyword)).order_by('-id')
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(ParentSearchListView, self).get_context_data(**kwargs)
        return context	
			
# 家長
class ParentChildListView(ListView):
    context_object_name = 'users'
    template_name = 'account/parent_child.html'
		
    def get_queryset(self):    
        queryset = Parent.objects.filter(parent_id=self.request.user.id)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(ParentChildListView, self).get_context_data(**kwargs)
        return context				
			
# Ajax 設為教師、取消教師
def parent_make(request):
    user_id = request.POST.get('userid')
    student_id = request.POST.get('studentid')
    action = request.POST.get('action')
    if user_id and action :
        user_id = int(user_id)
        student_id = int(student_id)
        user_student = User.objects.get(id=student_id)
        user_parent = User.objects.get(id=user_id)				
        if action == 'set':
            parents = Parent.objects.filter(student_id=student_id, parent_id=user_id)	
            if len(parents) == 0:
                parent = Parent(student_id=student_id, parent_id=user_id)
                parent.save()	
                # 記錄系統事件
                log = Log(user_id=student_id, event=u'<'+user_student.first_name+u'>設為家長<'+user_parent.first_name+'>')
                log.save()                        
                # create Message
                title = "<" + user_student.first_name + u">設您為家長"
                url = "/account/forum/"+ str(student_id)
                message = Message.create(title=title, url=url, time=timezone.now())
                message.save()                        
                    
                # message for group member
                messagepoll = MessagePoll.create(message_id = message.id,reader_id=user_id)
                messagepoll.save()    
        else : 
            # 記錄系統事件
            if is_event_open(request) :       							
                log = Log(user_id=student_id, event=u'<'+user_student.first_name+u'>取消家長<'+user_parent.first_name+'>')
                log.save()              
            parents = Parent.objects.filter(student_id=student_id, parent_id=user_id)
            for parent in parents:
                parent.delete()
            # create Message
            title = "<"+ request.user.first_name + u">取消您為冢長"
            url = "/"
            message = Message.create(title=title, url=url, time=timezone.now())
            message.save()                        
                    
            # message for group member
            messagepoll = MessagePoll.create(message_id = message.id,reader_id=user_id)
            messagepoll.save()               
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)        

#新增一個教師公告
class TeacherPostCreateView(CreateView):
    model = Message
    context_object_name = 'messages'    
    form_class = LineForm
    template_name = 'account/teacher_form.html'     

    def form_valid(self, form):
        teachers = Group.objects.get(name="teacher").user_set.all()
        self.object = form.save(commit=False)
        user_name = User.objects.get(id=self.request.user.id).first_name
        self.object.title = u"[系統]" + user_name + ":" + self.object.title
        self.object.author_id = self.request.user.id
        self.object.reader_id = self.request.user.id
        self.object.type = 3
        self.object.save()
        self.object.url = "/account/line/detail/0/" + str(self.object.id)
        self.object.classroom_id = 0
        self.object.save()
        if self.request.FILES:
            for file in self.request.FILES.getlist('files'):
                content = MessageContent()
                fs = FileSystemStorage()
                filename = uuid4().hex
                content.title = file.name
                content.message_id = self.object.id
                content.filename = str(self.request.user.id)+"/"+filename
                fs.save("static/upload/"+str(self.request.user.id)+"/"+filename, file)
                content.save()
        # 訊息
        for teacher in teachers:
            messagepoll = MessagePoll(message_id=self.object.id, reader_id=teacher.id, message_type=3, classroom_id=0)
            messagepoll.save()
        # 記錄系統事件
        if is_event_open(self.request) :            
            log = Log(user_id=self.request.user.id, event=u'新增教師公告<'+self.object.title+'>')
            log.save()                
        return redirect("/account/line/")      
        
    def get_context_data(self, **kwargs):
        context = super(TeacherPostCreateView, self).get_context_data(**kwargs)
        teachers = Group.objects.get(name="teacher").user_set.all()
        context['teachers'] = teachers
        return context	 

# Create your views here.
def import_sheet(request):
    if request.user.id != 1:
        return redirect("/")
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            ImportUser.objects.all().delete()
            request.FILES['file'].save_to_database(
                name_columns_by_row=0,
                model=ImportUser,
                mapdict=['username', 'first_name', 'password', 'email'])
            users = ImportUser.objects.all()
            return render(request, 'account/import_user.html',{'users':users})
        else:
            return HttpResponseBadRequest()
    else:	
        form = UploadFileForm()
    return render(
        request,
        'account/upload_form.html',
        {
            'form': form,
            'title': 'Excel file upload and download example',
            'header': ('Please choose any excel file ' +
                       'from your cloned repository:')
        })
	
# Create your views here.
def import_user(request):
    if request.user.id != 1:
        return redirect("/")
           
    users = ImportUser.objects.all()
    for user in users:
        try:
            account = User.objects.get(username=user.username)
        except ObjectDoesNotExist:
            new_user = User(username=user.username, first_name=user.first_name, password=user.password, email=user.email)
            # Set the chosen password                 
            new_user.set_password(user.password)
            # Save the User object
            new_user.save()
            profile = Profile(user=new_user)
            profile.save()          
     
            # create Message
            title = "請洽詢任課教師課程名稱及選課密碼"
            url = "/student/classroom/add"
            message = Message.create(title=title, url=url, time=timezone.now())
            message.save()                        
                    
            # message for group member
            messagepoll = MessagePoll.create(message_id = message.id,reader_id=new_user.id)
            messagepoll.save()               
    return redirect('/account/userlist')	
