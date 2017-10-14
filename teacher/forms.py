# -*- coding: utf-8 -*-
from django import forms
from account.models import Message
from teacher.models import Classroom, TWork, FWork, FContent, FClass, SpeculationWork, SpeculationContent, SpeculationClass, SpeculationAnnotation, ClassroomGroup


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
						
# 新增一個分組表單
class GroupForm(forms.ModelForm):
        class Meta:
           model = ClassroomGroup
           fields = ['title','numbers', 'assign']
        
        def __init__(self, *args, **kwargs):
            super(GroupForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "分組名稱"							
            self.fields['numbers'].label = "分組數目"	
						
# 新增一個分組表單
class GroupForm2(forms.ModelForm):
        class Meta:
           model = ClassroomGroup
           fields = ['title','numbers']
        
        def __init__(self, *args, **kwargs):
            super(GroupForm2, self).__init__(*args, **kwargs)
            self.fields['title'].label = "分組名稱"							
            self.fields['numbers'].label = "分組數目"	
