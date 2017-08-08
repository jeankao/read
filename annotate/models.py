# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from teacher.models import Classroom
from django.utils import timezone
from django.http import JsonResponse
import json

class Annotation(models.Model):
  user_id     = models.IntegerField(default=0)
  # annotation: 由 annotatejs 產生的標註內容
  annotation  = models.TextField(default='')
  # created: 建立時間
  created     = models.DateTimeField(default=timezone.now)
  # modified: 最後修改時間
  updated     = models.DateTimeField(default=timezone.now)
  # findex: 討論區id
  findex      = models.IntegerField(default=0)
  # stu_id: 學生id
  stuid       = models.IntegerField(default=0)  
  
  def __unicode__(self):
    user = User.objects.filter(id=self.user_id)[0]
    annotation_obj = json.loads(self.annotation)    
    return user.first_name+" : "+annotation_obj["text"]