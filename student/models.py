# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from teacher.models import Classroom
from django.utils import timezone
from django.http import JsonResponse
import json

# 學生選課資料
class Enroll(models.Model):
    # 學生序號
    student_id = models.IntegerField(default=0)
    # 班級序號
    classroom_id = models.IntegerField(default=0)
    # 座號
    seat = models.IntegerField(default=0)
    # 組別
    group = models.IntegerField(default=0)
    @property
	
    def classroom(self):
        return Classroom.objects.get(id=self.classroom_id)  

    @property        
    def student(self):
        return User.objects.get(id=self.student_id)      

    def __str__(self):
        return str(self.id)+":"+str(self.classroom_id)    

    class Meta:
        unique_together = ('student_id', 'classroom_id',)		
    
# 學生組別    
class EnrollGroup(models.Model):
    name = models.CharField(max_length=30)
    classroom_id = models.IntegerField(default=0)

#作業
class SFWork(models.Model):
    student_id = models.IntegerField(default=0)
    index = models.IntegerField()
    memo = models.TextField(default='')
    memo_e =  models.IntegerField(default=0)
    memo_c = models.IntegerField(default=0)		
    publish = models.BooleanField(default=False)
    publication_date = models.DateTimeField(default=timezone.now)
    reply_date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=0)
    scorer = models.IntegerField(default=0)
    comment = models.TextField(default='',null=True,blank=True)
    comment_publication_date = models.DateTimeField(default=timezone.now)		
    likes = models.TextField(default='')
    like_count = models.IntegerField(default=0)	
    reply = models.IntegerField(default=0)
		
    def __unicode__(self):
        user = User.objects.filter(id=self.student_id)[0]
        index = self.index
        return user.first_name+"("+str(index)+")"

class SFContent(models.Model):
    index =  models.IntegerField(default=0)
    student_id = models.IntegerField(default=0)
    work_id = models.IntegerField(default=0)
    title =  models.CharField(max_length=250,null=True,blank=True)
    filename = models.CharField(max_length=60,null=True,blank=True)    
    publication_date = models.DateTimeField(default=timezone.now)
    delete_date = models.DateTimeField(default=timezone.now)		
    visible = models.BooleanField(default=True)

#討論留言
class SFReply(models.Model):
    index = models.IntegerField(default=0)
    work_id =  models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    memo =  models.TextField(default='')
    publication_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.memo

		
#思辨文章
class SSpeculationWork(models.Model):
    student_id = models.IntegerField(default=0)
    index = models.IntegerField()
    memo = models.TextField(default='')
    publish = models.BooleanField(default=False)
    publication_date = models.DateTimeField(default=timezone.now)
    reply_date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=0)
    scorer = models.IntegerField(default=0)
    comment = models.TextField(default='',null=True,blank=True)
    comment_publication_date = models.DateTimeField(default=timezone.now)	
    likes = models.TextField(default='')
    like_count = models.IntegerField(default=0)	
    reply = models.IntegerField(default=0)
		
    def __unicode__(self):
        user = User.objects.filter(id=self.student_id)[0]
        index = self.index
        return user.first_name+"("+str(index)+")"

class SSpeculationContent(models.Model):
    index =  models.IntegerField(default=0)
    student_id = models.IntegerField(default=0)
    work_id = models.IntegerField(default=0)
    title =  models.CharField(max_length=250,null=True,blank=True)
    filename = models.CharField(max_length=60,null=True,blank=True)    
    publication_date = models.DateTimeField(default=timezone.now)
    delete_date = models.DateTimeField(default=timezone.now)		
    visible = models.BooleanField(default=True)

class StudentGroup(models.Model):
    group_id = models.IntegerField(default=0)
    enroll_id = models.IntegerField(default=0)
    group = models.IntegerField(default=0)		

    class Meta:
        unique_together = ('enroll_id', 'group_id',)		

class StudentGroupLeader(models.Model):
    group_id = models.IntegerField(default=0)
    group = models.IntegerField(default=0)	
    enroll_id = models.IntegerField(default=0)	

    class Meta:
        unique_together = ('group_id', 'group')		        		

#測驗
class ExamWork(models.Model):
    student_id = models.IntegerField(default=0)
    exam_id = models.IntegerField()    
    questions = models.TextField(default='')
    publish = models.BooleanField(default=False)
    publication_date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=0)
    scorer = models.IntegerField(default=0)
		
    def __unicode__(self):
        user = User.objects.filter(id=self.student_id)[0]
        exam_id = self.exam_id
        return user.first_name+"("+str(exam_id)+")"		
			
#測驗答案
class ExamAnswer(models.Model):
    examwork_id = models.IntegerField(default=0)
    question_id = models.IntegerField(default=0)
    student_id = models.IntegerField(default=0)
    answer = models.TextField(default='')
    answer_right = models.BooleanField(default=False)
		
    class Meta:
        unique_together = ('student_id', 'examwork_id', 'question_id')		
		
class TeamContent(models.Model):
    team_id =  models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)  
    types = models.IntegerField(default=0)
    title = models.CharField(max_length=250,null=True,blank=True)
    memo = models.TextField(default='')
    link = models.CharField(max_length=250,null=True,blank=True)
    youtube = models.CharField(max_length=250,null=True,blank=True)
    youtube_length = models.IntegerField(default=0)
    file = models.FileField(blank=True,null=True)
    filename = models.CharField(max_length=60,null=True,blank=True)
    publication_date = models.DateTimeField(default=timezone.now)    
    publish = models.BooleanField(default=False)

class CourseContentProgress(models.Model):
    student_id = models.IntegerField(default=0)  
    content_id = models.IntegerField(default=0)  
    progress =models.IntegerField(default=0)  
    start_time = models.DateTimeField(default=timezone.now)    
    finish_time = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student_id', 'content_id')		    
      