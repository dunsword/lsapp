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
    pass
            
class TopicService():
    PAGE_SIZE=10
    
    def getTopicForm(self,topic):
        topicForm=TopicForm(instance=topic)
        return topicForm
    
    def addReply(self,replyForm):
        '''
            replyForm should has been validated
        '''
        topicid=replyForm.cleaned_data['topicid']
        #这里应该优化为直接加reply_count，而不是取出整个对象
        topic=Topic.objects.get(pk=topicid)
        topic.reply_count +=1
        replyForm.save()
        topic.save()
        return replyForm
    
    def getPageCount(self,topic):
        pc = topic.reply_count/(TopicService.PAGE_SIZE)
        if pc*TopicService.PAGE_SIZE < topic.reply_count:
            pc+=1
        return pc
        
    def getTopicReplyList(self,topicId,page=1):
        if page<1:
            page=1
        start=(page-1)*TopicService.PAGE_SIZE
        end=page*TopicService.PAGE_SIZE-1
        replyList= TopicReply.objects.filter(topicid__exact=topicId)[start:end]
        for reply in replyList:
            start+=1 #start 从0开始，所以先加1
            reply.num=start
        return replyList
            