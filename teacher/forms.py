# -*- coding: utf-8 -*-
from django import forms
from account.models import Message
from teacher.models import Classroom, FWork, FContent, FClass, SpeculationWork, SpeculationContent, SpeculationClass, SpeculationAnnotation, ClassroomGroup, Exam, ExamClass, ExamQuestion
from teacher.models import TeamWork, TeamClass


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
class ForumCategroyForm(forms.ModelForm):
        class Meta:
           model = FWork
           fields = ['domains', 'levels']
        
        def __init__(self, *args, **kwargs):
            super(ForumCategroyForm, self).__init__(*args, **kwargs)			
						
# 新增一個繳交期長表單
class ForumDeadlineForm(forms.ModelForm):
        class Meta:
           model = FClass
           fields = ['deadline', 'deadline_date']
        
        def __init__(self, *args, **kwargs):
            super(ForumDeadlineForm, self).__init__(*args, **kwargs)			

						
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

# 新增一個測驗
class ExamForm(forms.ModelForm):
        class Meta:
           model = Exam                    
           fields = ['title']
        
        def __init__(self, *args, **kwargs):
            super(ExamForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "測驗主題"
            self.fields['title'].widget.attrs.update({'class' : 'form-control list-group-item-text'})							
												
# 新增一個測驗分類表單
class ExamCategroyForm(forms.ModelForm):
        class Meta:
           model = Exam
           fields = ['domains', 'levels']
        
        def __init__(self, *args, **kwargs):
            super(ExamCategroyForm, self).__init__(*args, **kwargs)										

# 新增一個繳交期長表單
class ExamDeadlineForm(forms.ModelForm):
        class Meta:
           model = ExamClass
           fields = ['deadline', 'deadline_date']
        
        def __init__(self, *args, **kwargs):
            super(ExamDeadlineForm, self).__init__(*args, **kwargs)								
						
# 新增一個題目
class ExamQuestionForm(forms.ModelForm):
        class Meta:
           model = ExamQuestion
           fields = ['exam_id', 'types', 'title', 'option1', 'option2', 'option3', 'option4', 'answer', 'score']
        
        def __init__(self, *args, **kwargs):
            super(ExamQuestionForm, self).__init__(*args, **kwargs)
            self.fields['exam_id'].required = False		
            self.fields['title'].required = False						
            self.fields['option1'].required = False
            self.fields['option2'].required = False
            self.fields['option3'].required = False
            self.fields['option4'].required = False
            self.fields['answer'].required = False			
            self.fields['score'].required = False				


#上傳檔案
class UploadFileForm(forms.Form):
    file = forms.FileField()						
		
# 新增一個任務
class TeamForm(forms.ModelForm):
        class Meta:
           model = TeamWork
           fields = ['title']
        
        def __init__(self, *args, **kwargs):
            super(TeamForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "任務主題"
            self.fields['title'].widget.attrs.update({'class' : 'form-control list-group-item-text'})									
		
# 新增一個課程表單
class TeamCategroyForm(forms.ModelForm):
        class Meta:
           model = TeamWork
           fields = ['domains', 'levels']
        
        def __init__(self, *args, **kwargs):
            super(TeamCategroyForm, self).__init__(*args, **kwargs)			
						
# 新增一個繳交期限表單
class TeamDeadlineForm(forms.ModelForm):
        class Meta:
           model = TeamClass
           fields = ['deadline', 'deadline_date']
        
        def __init__(self, *args, **kwargs):
            super(TeamDeadlineForm, self).__init__(*args, **kwargs)			

		