# -*- coding: utf-8 -*-
from django import forms
from teacher.models import Classroom
from student.models import Enroll, EnrollGroup, SWork, SFWork

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
          
class SubmitForm(forms.ModelForm):
        class Meta:
           model = SWork
           fields = ['youtube','memo']
      
        def __init__(self, *args, **kwargs):
            super(SubmitForm, self).__init__(*args, **kwargs)
            self.fields['youtube'].label = "影片網址"
            self.fields['memo'].label = "心得感想"

class ForumSubmitForm(forms.Form):
        memo =  forms.CharField(required=False)
        file = forms.FileField(required=False)
      
        def __init__(self, *args, **kwargs):
            super(ForumSubmitForm, self).__init__(*args, **kwargs)
            self.fields['memo'].label = "心得感想"
            self.fields['file'].label = "檔案"

class SpeculationSubmitForm(forms.Form):
        memo =  forms.CharField(required=False)
        file = forms.FileField(required=False)
      
        def __init__(self, *args, **kwargs):
            super(SpeculationSubmitForm, self).__init__(*args, **kwargs)
            self.fields['memo'].label = "心得感想"
            self.fields['file'].label = "檔案"
