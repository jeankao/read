# -*- coding: utf-8 -*-
from django import forms
from teacher.models import *
from student.models import *

class EnrollForm(forms.Form):
        password =  forms.CharField()
        seat = forms.CharField()
        
        def __init__(self, *args, **kwargs):
            super(EnrollForm, self).__init__(*args, **kwargs)
            self.fields['password'].label = "選課密碼"
            self.fields['seat'].label = "座號"
   
            
class SeatForm(forms.ModelForm):
        class Meta:
            model = Enroll
            fields = ['seat']
          
class ForumSubmitForm(forms.Form):
        memo =  forms.CharField(required=False)
        memo_e =  forms.IntegerField(required=False)
        memo_c =  forms.IntegerField(required=False)      
        file = forms.FileField(required=False)
      
        def __init__(self, *args, **kwargs):
            super(ForumSubmitForm, self).__init__(*args, **kwargs)
            self.fields['memo'].label = "心得感想"
            self.fields['memo_e'].label = "英文"
            self.fields['memo_c'].label = "中文"            
            self.fields['file'].label = "檔案"

class SpeculationSubmitForm(forms.Form):
        memo =  forms.CharField(required=False)
        file = forms.FileField(required=False)
      
        def __init__(self, *args, **kwargs):
            super(SpeculationSubmitForm, self).__init__(*args, **kwargs)
            self.fields['memo'].label = "心得感想"
            self.fields['file'].label = "檔案"

# 新增一個作業
class TeamContentForm(forms.ModelForm):
        class Meta:
           model = TeamContent
           fields = ['team_id', 'types', 'title', 'link', 'youtube', 'file', 'memo']
        
        def __init__(self, *args, **kwargs):
            super(TeamContentForm, self).__init__(*args, **kwargs)
            self.fields['team_id'].required = False		
            self.fields['title'].required = False						
            self.fields['link'].required = False
            self.fields['youtube'].required = False
            self.fields['file'].required = False
            self.fields['memo'].required = False	