# -*- coding: UTF-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Round(models.Model):
    classroom_id = models.IntegerField(default=0)
    gourp_id = models.IntegerField(default=0)
    publish = models.DateTimeField(default=timezone.now)    

# 分組作品
class ShowGroup(models.Model):
    round_id = models.IntegerField(default=0)
    youtube = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    open =  models.BooleanField(default=False)
	
# 評分
class ShowReview(models.Model):
    show_id = models.IntegerField(default=0)
    student_id = models.IntegerField(default=0)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    score3 = models.IntegerField(default=0)
    comment = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    done = models.BooleanField(default=False)	
	
    @property        
    def student(self):
        return User.objects.get(id=self.student_id)      