# -*- coding: utf-8 -*-
from django import forms
from account.models import Message
from teacher.models import Classroom, TWork, FWork, FContent, FClass, SpeculationWork, SpeculationContent, SpeculationClass, SpeculationAnnotation
from student.models import SWork


# 新增一個課程表單
class ClassroomForm(forms.ModelForm):
        class Meta:
           model = Classroom
           fields = ['name','password', 'domains', 'levels']
        
        def __init__(self, *args, **kwargs):
            super(ClassroomForm, self).__init__(*args, **kwargs)
            self.fields['name'].label = "班級名稱1"
            self.fields['password'].label = "選課密碼"
            self.fields['name'].widget.attrs.update({'class' : 'form-control list-group-item-text'})						
						
# 新增一個課程表單
class CategroyForm(forms.ModelForm):
        class Meta:
           model = FWork
           fields = ['domains', 'levels']
        
        def __init__(self, *args, **kwargs):
            super(CategroyForm, self).__init__(*args, **kwargs)			
						
# 新增一個繳交期長表單
class DeadlineForm(forms.ModelForm):
        class Meta:
           model = FClass
           fields = ['deadline', 'deadline_date']
        
        def __init__(self, *args, **kwargs):
            super(DeadlineForm, self).__init__(*args, **kwargs)			

# 新增一個作業
class WorkForm(forms.ModelForm):
        class Meta:
           model = TWork
           fields = ['title']
        
        def __init__(self, *args, **kwargs):
            super(WorkForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "作業名稱"
            
# 作業評分表單           
class ScoreForm(forms.ModelForm):
        RELEVANCE_CHOICES = (
            (100, "你好棒(100分)"),
            (90, "90分"),
            (80, "80分"),
            (70, "70分"),
            (60, "60分"),
        )
        score = forms.ChoiceField(choices = RELEVANCE_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        assistant = forms.BooleanField(required=False,label="小老師")
    
        class Meta:
           model = SWork
           fields = ['score']
		   
        def __init__(self, user, *args, **kwargs): 
            super(ScoreForm, self).__init__(*args, **kwargs)	
            if user.groups.all().count() == 0 :
                del self.fields['assistant']
Check_CHOICES = (
    (100, "你好棒(100分)"),
    (90, "90分"),
    (80, "80分"),
    (70, "70分"),
    (60, "60分"),
    (40, "40分"),
    (20, "20分"),
    (0, "0分"),			
)		

# 新增一個作業
class ForumForm(forms.ModelForm):
        class Meta:
           model = FWork
           fields = ['title']
        
        def __init__(self, *args, **kwargs):
            super(ForumForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "討論主題"
            self.fields['title'].widget.attrs.update({'class' : 'form-control list-group-item-text'})									
						
# 新增一個作業
class ForumContentForm(forms.ModelForm):
        class Meta:
           model = FContent
           fields = ['forum_id', 'types', 'title', 'link', 'youtube', 'file', 'memo']
        
        def __init__(self, *args, **kwargs):
            super(ForumContentForm, self).__init__(*args, **kwargs)
            self.fields['forum_id'].required = False		
            self.fields['title'].required = False						
            self.fields['link'].required = False
            self.fields['youtube'].required = False
            self.fields['file'].required = False
            self.fields['memo'].required = False						
						
# 新增一個課程表單
class AnnounceForm(forms.ModelForm):
        class Meta:
           model = Message
           fields = ['title', 'content']
        
        def __init__(self, *args, **kwargs):
            super(AnnounceForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "公告主旨"
            self.fields['title'].widget.attrs['size'] = 50	
            self.fields['content'].required = False							
            self.fields['content'].label = "公告內容"
            self.fields['content'].widget.attrs['cols'] = 50
            self.fields['content'].widget.attrs['rows'] = 20        
            self.fields['title'].widget.attrs.update({'class' : 'form-control list-group-item-text'})      						
						

# 新增一個文章
class SpeculationForm(forms.ModelForm):
        class Meta:
           model = SpeculationWork
           fields = ['title']
        
        def __init__(self, *args, **kwargs):
            super(SpeculationForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "文章主題"
            self.fields['title'].widget.attrs.update({'class' : 'form-control list-group-item-text'})									
						
# 新增一個文章
class SpeculationContentForm(forms.ModelForm):
        class Meta:
           model = SpeculationContent
           fields = ['forum_id', 'types', 'text', 'youtube', 'file', 'memo', 'title', 'link']
        
        def __init__(self, *args, **kwargs):
            super(SpeculationContentForm, self).__init__(*args, **kwargs)
            self.fields['forum_id'].required = False		
            self.fields['text'].required = False
            self.fields['youtube'].required = False
            self.fields['file'].required = False
            self.fields['memo'].required = False						
            self.fields['link'].required = False
            self.fields['title'].required = False										

# 新增一個註記類別
class SpeculationAnnotationForm(forms.ModelForm):
        class Meta:
           model = SpeculationAnnotation
           fields = ['forum_id', 'kind', 'color']
        
        def __init__(self, *args, **kwargs):
            super(SpeculationAnnotationForm, self).__init__(*args, **kwargs)
