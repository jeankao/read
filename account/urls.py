# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        # post views
        url(r'^dashboard/$',  views.MessageListView.as_view(), name='dashboard'),  
        #登入
        url(r'^login/$', views.user_login, name='login'),
        #註冊帳號
        url(r'^register/$', views.register, name='register'),
        #登出
        url(r'^logout/$',auth_views.logout),
        #列出所有帳號
        url(r'^userlist/$', views.UserListView.as_view()),
]