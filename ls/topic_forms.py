# coding=utf-8

    
from django import forms
from ls.models import Topic,TopicReply

class TopicForm(forms.ModelForm):
        class Meta:
            model=Topic
    
class TopicReplyForm(forms.ModelForm):
        class Meta:
            model=TopicReply