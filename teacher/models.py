# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# 班級
class Classroom(models.Model):
    # 班級名稱
    name = models.CharField(max_length=30)
    # 選課密碼
    password = models.CharField(max_length=30)
    # 授課教師
    teacher_id = models.IntegerField(default=0)
    # 學習領域
    domains = models.TextField(default='')  
    #年級
    levels = models.TextField(default='') 
    
    @property
    def teacher(self):
        return User.objects.get(id=self.teacher_id)  
        
    def __unicode__(self):
        return self.name
      
#班級助教
class Assistant(models.Model):
    classroom_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
      
#課程
class TWork(models.Model):
    title = models.CharField(max_length=250)
    teacher_id = models.IntegerField(default=0)		
    classroom_id = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now) 
    
#討論區
class FWork(models.Model):
    title = models.CharField(max_length=250,verbose_name= '討論主題')
    teacher_id = models.IntegerField(default=0)		
    classroom_id = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now) 
    domains = models.TextField(default='')    
    levels = models.TextField(default='')    

def get_deadline():
    return datetime.today() + timedelta(days=14)		
		
class FClass(models.Model):
    forum_id = models.IntegerField(default=0)
    classroom_id =  models.IntegerField(default=0)
    publication_date = models.DateTimeField(default=timezone.now)
    deadline = models.BooleanField(default=False)
    deadline_date = models.DateTimeField(default=get_deadline)
	
    def __unicode__(self):
        return str(self.forum_id)	

class FContent(models.Model):
    forum_id =  models.IntegerField(default=0)
    types = models.IntegerField(default=0)
    title = models.CharField(max_length=250,null=True,blank=True)
    memo = models.TextField(default='')    
    link = models.CharField(max_length=250,null=True,blank=True) 
    youtube = models.CharField(max_length=250,null=True,blank=True) 
    file = models.FileField(blank=True,null=True)
    filename = models.CharField(max_length=60,null=True,blank=True)     
		
#思辨區
class SpeculationWork(models.Model):
    title = models.CharField(max_length=250,verbose_name= '思辨主題')
    teacher_id = models.IntegerField(default=0)		
    classroom_id = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now) 
    domains = models.TextField(default='')    
    levels = models.TextField(default='') 

		
def get_deadline():
    return datetime.today() + timedelta(days=14)		
		
class SpeculationClass(models.Model):
    forum_id = models.IntegerField(default=0)
    classroom_id =  models.IntegerField(default=0)
    publication_date = models.DateTimeField(default=timezone.now)
    deadline = models.BooleanField(default=False)
    deadline_date = models.DateTimeField(default=get_deadline)
    group =  models.IntegerField(default=0)		
	
    def __unicode__(self):
        return str(self.forum_id)	

class SpeculationContent(models.Model):
    forum_id =  models.IntegerField(default=0)
    types = models.IntegerField(default=0)
    title = models.CharField(max_length=250,null=True,blank=True)
    memo = models.TextField(default='')    
    text = models.TextField(default='')
    link = models.CharField(max_length=250,null=True,blank=True) 		
    youtube = models.CharField(max_length=250,null=True,blank=True) 
    file = models.FileField(blank=True,null=True)
    filename = models.CharField(max_length=60,null=True,blank=True)     
		
class SpeculationAnnotation(models.Model):
    forum_id =  models.IntegerField(default=0)
    kind = models.CharField(max_length=250,null=True,blank=True)
    color = models.CharField(max_length=7,null=True,blank=True)
		
class ClassroomGroup(models.Model):
    # 班級
    classroom_id = models.IntegerField(default=0)
    #分組名稱
    title = models.CharField(max_length=250,null=True,blank=True)    
    #小組數目
    numbers = models.IntegerField(default=6)
    #開放分組
    opening = models.BooleanField(default=True)
		#分組方式
    assign = models.IntegerField(default=0)
       
    def __unicode__(self):
        return self.classroom_id

#測驗
class Exam(models.Model):
    title = models.CharField(max_length=250,verbose_name= '測驗主題')
    user_id = models.IntegerField(default=0)		
    classroom_id = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now) 
    domains = models.TextField(default='')    
    levels = models.TextField(default='')    	
	
class ExamClass(models.Model):
    exam_id = models.IntegerField(default=0)
    classroom_id =  models.IntegerField(default=0)
    publication_date = models.DateTimeField(default=timezone.now)
    deadline = models.BooleanField(default=False)
    deadline_date = models.DateTimeField(default=get_deadline)
	
    def __unicode__(self):
        return str(self.exam_id)
			
class ExamQuestion(models.Model):
    exam_id = models.IntegerField(default=0)
    types = models.IntegerField(default=0)
    title = models.TextField(default='')    		
    option1 = models.CharField(max_length=250,null=True,blank=True)
    option2 = models.CharField(max_length=250,null=True,blank=True)		
    option3 = models.CharField(max_length=250,null=True,blank=True)		
    option4 = models.CharField(max_length=250,null=True,blank=True)		
    answer = models.IntegerField(default=0)		
    answer_text = models.TextField(default='')    				
		