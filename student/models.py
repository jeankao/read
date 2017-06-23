# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from teacher.models import Classroom
from django.utils import timezone

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
        return str(self.id)    

    class Meta:
        unique_together = ('student_id', 'classroom_id',)		
    
# 學生組別    
class EnrollGroup(models.Model):
    name = models.CharField(max_length=30)
    classroom_id = models.IntegerField(default=0)
		
#作業
class SWork(models.Model):
    student_id = models.IntegerField(default=0)
    index = models.IntegerField()
    youtube = models.CharField(max_length=100)	
    memo = models.TextField(default='')
    publication_date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=-1)
    scorer = models.IntegerField(default=0)
		
    def __unicode__(self):
        user = User.objects.filter(id=self.student_id)[0]
        index = self.index
        return user.first_name+"("+str(index)+")"		
			
# 小老師        
class Assistant(models.Model):
    student_id = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    lesson = models.IntegerField(default=0)
    
    @property        
    def student(self):
        return User.objects.get(id=self.student_id)   

#作業
class SFWork(models.Model):
    student_id = models.IntegerField(default=0)
    index = models.IntegerField()
    memo = models.TextField(default='')
    publication_date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=-1)
    scorer = models.IntegerField(default=0)
		
    def __unicode__(self):
        user = User.objects.filter(id=self.student_id)[0]
        index = self.index
        return user.first_name+"("+str(index)+")"		