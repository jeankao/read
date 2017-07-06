# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
      
#搜查線
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

class FClass(models.Model):
    forum_id = models.IntegerField(default=0)
    classroom_id =  models.IntegerField(default=0)
    publication_date = models.DateTimeField(default=timezone.now)
	
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
    filename = models.CharField(max_length=20,null=True,blank=True)     