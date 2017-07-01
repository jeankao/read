# -*- coding: UTF-8 -*-
from django import template
from django.contrib.auth.models import User
from account.models import MessagePoll
from teacher.models import Classroom
from student.models import Enroll, SFWork, SFReply
from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.safestring import mark_safe
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
import re
import json
register = template.Library()

@register.filter
def modulo(num, val):
    return num % val
  
@register.filter
def realname(user_id):
    try: 
        user = User.objects.get(id=user_id)
        return user.first_name
    except ObjectDoesNotExist:
        pass
        return ""
  
@register.filter(name="img")
def img(title):
    if title.startswith(u'[私訊]'):
        return "line"
    elif title.startswith(u'[公告]'):
        return "announce"
    elif u'擔任小老師' in title:
        return "assistant"
    elif u'設您為教師' in title:
        return "teacher"
    elif u'核發了一張證書給你' in title:
        return "certificate"
    else :
        return ""
 
@register.filter(name='has_group') 
def has_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name) 
    except ObjectDoesNotExist:
        group = None
    return group in user.groups.all()

@register.filter()
def number(youtube):
    number_pos = youtube.find("v=")
    number = youtube[number_pos+2:number_pos+13]
    return number

@register.filter()
def memo(text):
  memo = re.sub(r"\n", r"<br/>", re.sub(r"\[m_(\d+)#(\d\d:\d\d:\d\d)\]", r"<button class='btn btn-default btn-xs btn-marker' data-mid='\1' data-time='\2'>\2</button>",text))
  return memo

@register.filter()
def likes(work_id):
    sfwork = SFWork.objects.get(id=work_id)
    jsonDec = json.decoder.JSONDecoder()    
    if sfwork.likes:
        likes = jsonDec.decode(sfwork.likes)
        return likes
    return []
  
@register.filter()
def is_pic(title):   
    if title[-3:].upper() == "PNG":
        return True
    if title[-3:].upper() == "JPG":
        return True   
    if title[-3:].upper() == "GIF":
        return True            
    return False
