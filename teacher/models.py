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
    # 是否開放分組
    group_open = models.BooleanField(default=True)
    # 組別人數
    group_size = models.IntegerField(default=4)

    @property
    def teacher(self):
        return User.objects.get(id=self.teacher_id)  
        
    def __unicode__(self):
        return self.name
      
#搜查線
class TWork(models.Model):
    title = models.CharField(max_length=250)
    teacher_id = models.IntegerField(default=0)		
    classroom_id = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)    
    
#討論區
class FWork(models.Model):
    title = models.CharField(max_length=250)
    teacher_id = models.IntegerField(default=0)		
    classroom_id = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)    

class FContent(models.Model):
    forum_id =  models.IntegerField(default=0)
    content_type = models.IntegerField(default=0)
    content_title = models.CharField(max_length=250,null=True,blank=True)     
    content_link = models.CharField(max_length=250,null=True,blank=True) 
    content_youtube = models.CharField(max_length=250,null=True,blank=True) 
    content_file = models.FileField(blank=True,null=True)
    content_filename = models.CharField(max_length=20,null=True,blank=True)     