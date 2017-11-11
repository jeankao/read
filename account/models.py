# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class Site(models.Model):
  # 訪客人次
	home_count = models.IntegerField(default=0)
	visitor_count = models.IntegerField(default=0)
	# 開站時間
	open_time = models.DateTimeField(auto_now_add=True)
	# 網站名稱
	site_name = models.CharField(max_length=50)
	# 網站圖片
	site_image =  models.CharField(max_length=255)

# 個人檔案資料
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name="profile")
	#user_id = models.IntegerField(default=0)
	# 積分：上傳作業
	work = models.IntegerField(default=0)
	# 積分：按讚
	like = models.FloatField(default=0.0)
	# 積分：留言
	reply = models.FloatField(default=0.0)
	# 大頭貼等級
	avatar = models.IntegerField(default=0)

	def __unicode__(self):
		return str(self.user_id)
	
# 積分記錄 
class PointHistory(models.Model):
    # 使用者序號
	user_id = models.IntegerField(default=0)
	# 積分類別 
	kind = models.IntegerField(default=0)
	# 積分項目
	message = models.CharField(max_length=100)
	# 將積分項目超連結到某個頁面
	url = models.CharField(max_length=100)
	# 記載時間 
	publish = models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return str(self.user_id)
		
# 系統記錄
class Log(models.Model):
    # 使用者序號
    user_id = models.IntegerField(default=0)
		# 影片編號
    youtube_id = models.IntegerField(default=0)
    # 事件內容
    event = models.CharField(max_length=100)
	  # 發生時間 
    publish = models.DateTimeField(default=timezone.now)

    @property
    def user(self):
        return User.objects.get(id=self.user_id)
	
    def __unicode__(self):
        return str(self.user_id)+'--'+self.event

# 大廳訊息	
class Message(models.Model):
    author_id = models.IntegerField(default=0)
    reader_id = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    title = models.CharField(max_length=250)
    content = models.TextField(default='')
    url = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
    #    return self.title
		
    @classmethod
    def create(cls, title, url, time):
        message = cls(title=title, url=url, time=time)
        return message
			
class MessageContent(models.Model):
    message_id =  models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    title =  models.CharField(max_length=250,null=True,blank=True)
    filename = models.CharField(max_length=250,null=True,blank=True)    
    publication_date = models.DateTimeField(default=timezone.now)

# 訊息    
class MessagePoll(models.Model):
    message_type = models.IntegerField(default=0)
    message_id = models.IntegerField(default=0)
    reader_id = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    read = models.BooleanField(default=False)
    
    @property
    def message(self):
        return Message.objects.get(id=self.message_id)
        
    @classmethod
    def create(cls, message_id, reader_id):
        messagepoll = cls(message_id=message_id, reader_id=reader_id)
        return messagepoll


class MessageFile(models.Model):
    message_id = models.IntegerField(default=0) 
    filename = models.TextField()
    before_name = models.TextField()
    upload_date = models.DateTimeField(default=timezone.now)
		
# 訪客 
class Visitor(models.Model):
    date = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    
# 訪客記錄
class VisitorLog(models.Model):
    visitor_id = models.IntegerField(default=0)    
    user_id = models.IntegerField(default=0)
    IP = models.CharField(max_length=20, default="")
    time = models.DateTimeField(auto_now_add=True)
    
# 學習領域
class Domain(models.Model):
	title = models.CharField(max_length=200, default="",verbose_name= '領域名稱')
	
# 年級
class Level(models.Model):
  title = models.CharField(max_length=200, default="",verbose_name= '年級')

# 家長
class Parent(models.Model):
  student_id = models.IntegerField(default=0)
  parent_id = models.IntegerField(default=0)
	
  class Meta:
      unique_together = ('student_id', 'parent_id',)		
			
#匯入
class ImportUser(models.Model):
	username = models.CharField(max_length=50, default="")
	first_name = models.CharField(max_length=50, default="")
	password = models.CharField(max_length=50, default="")
	email = models.CharField(max_length=100, default="")	
	