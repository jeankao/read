# -*- coding: UTF-8 -*-
from django import template
from django.contrib.auth.models import User
from account.models import MessagePoll, Site, Parent
from teacher.models import Classroom, Assistant
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
  
@register.filter(takes_context=True)
def realname(user_id):
    try: 
        user = User.objects.get(id=user_id)
        return user.first_name
    except ObjectDoesNotExist:
        pass
        return ""
      
@register.filter
def classname(classroom_id):
    try: 
        classroom = Classroom.objects.get(id=classroom_id)
        return classroom.name
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
  
@register.filter(name='assistant') 
def assistant(user_id):
    assistants = Assistant.objects.filter(user_id=user_id)
    if assistants:
      return True
    return False

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
  
@register.filter()
def int_to_str(number):   
    return str(number)

@register.filter()
def site_name(request):   
    return Site.objects.get(id=1).site_name
  
@register.filter()
def parent(user_id, student_id):
    parents = Parent.objects.filter(student_id=student_id, parent_id=user_id)
    if len(parents)> 0 :
      return True
    else:
      return False
    
@register.filter()
def is_parent(user_id):
    parents = Parent.objects.filter(parent_id=user_id)
    if len(parents)> 0 :
      return True
    else:
      return False
    
@register.filter(name='week') 
def week(date_number):
    year = date_number / 10000
    month = (date_number - year * 10000) / 100
    day = date_number - year * 10000 - month * 100
    now = datetime(year, month, day, 8, 0, 0)
    return now.strftime("%A")
  
@register.filter()
def classroom(user_id):
    if user_id > 0 :
        enrolls = Enroll.objects.filter(student_id=user_id).order_by("-id")[:5]
        classroom_names = ""
        for enroll in enrolls:
            classroom = Classroom.objects.get(id=enroll.classroom_id)
            classroom_names += classroom.name + "| "
        return classroom_names
    else : 
        return "匿名"
		