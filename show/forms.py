# -*- coding: utf-8 -*-
from django import forms
from show.models import ShowGroup, ShowReview
from teacher.models import Classroom
#from django.views.generic.edit import UpdateView

# 組別
class GroupForm(forms.ModelForm):
        class Meta:
           model = ShowGroup
           fields = ['round_id']
           
        def __init__(self, *args, **kwargs):
            super(GroupForm, self).__init__(*args, **kwargs)
            self.fields['name'].label = "組別名稱"

# 作品		
class ShowForm(forms.ModelForm):
        class Meta:
           model = ShowGroup
           fields = ['youtube']
           
        def __init__(self, *args, **kwargs):
            super(ShowForm, self).__init__(*args, **kwargs)
            self.fields['youtube'].label = "影片網址"						
            self.fields['youtube'].required = False
# 評分
class ReviewForm(forms.ModelForm):
        class Meta:
            model = ShowReview
            fields = ['score1', 'score2', 'score3', 'comment']
			
        def __init__(self, *args, **kwargs):
            super(ReviewForm, self).__init__(*args, **kwargs)
            self.fields['score1'].label = "問題意義與價值"
            self.fields['score2'].label = "分析複雜度"
            self.fields['score3'].label = "視覺化程度(清楚否)"
            self.fields['comment'].label = "評語"			 
            
 