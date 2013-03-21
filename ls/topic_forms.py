# coding=utf-8

    
from django import forms
from ls.models import Topic,TopicReply,Category

class TopicForm(forms.ModelForm):
        class Meta:
            model=Topic
        
        def __init__(self,instance=None):
            super(TopicForm,self).__init__(instance=instance)
            self.category=None
            
        def getCategory(self):
            if self.category:
                return self.category
            if self.is_valid():
                cid=self.cleaned_data['categoryid']
            elif self.instance:
                cid=self.instance.categoryid
            else:
                cid=None
            
            if cid or cid==0:
                self.category=Category.objects.get(pk=cid)
                return self.category
            
            self.category=None
            return None
        
class TopicReplyForm(forms.ModelForm):
        class Meta:
            model=TopicReply

class TopicReplyService():
    def getTopicReplyList(self,topicId,page=1):
        replyList= TopicReply.objects.filter(topicid__exact=topicId)[:20]
        return replyList
            
class TopicService():
    def getTopicForm(self,topicId):
        topic=Topic.objects.get(pk=topicId)
        topicForm=TopicForm(instance=topic)
        return topicForm
        