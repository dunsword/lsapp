# coding=utf-8

    
from django import forms
from ls.models import Topic,TopicReply,Category,Document
from django.forms.util import ErrorList

class TopicForm(forms.ModelForm):
        class Meta:
            model=Topic
            fields = ('userid','title', 'content','categoryid','catid1','catid2','like_count','read_count','reply_count','topic_type')
        
        def __init__(self,  prefix=None, instance=None,data=None):
            super(TopicForm,self).__init__(prefix=prefix, data=data, instance=instance)
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

class DocumentForm(forms.ModelForm):
       '''
       id=forms.IntegerField(label='docid',widget=forms.Field.hidden_widget)
       topicid=forms.IntegerField(label='topicid',widget=forms.Field.hidden_widget)
       title=forms.CharField(
                               label='标题',
                               min_length=1,
                               max_length=256,
                               error_messages={
                                               'required': '昵称不能为空！',
                                               'min_length':'标题不能为空！',
                                               'max_length': '不能超过256个字！'
                                               })
       ontent=forms.CharField(
                               label='内容摘要',
                               min_length=10,
                               max_length=1024,
                               error_messages={
                                               'required': '昵称不能为空！',
                                               'min_length':'不能少于10个字！',
                                               'max_length': '不能超过2000个字！'
                                               })
       
       author_name=forms.CharField(label='作者',
                                   max_length=256,
                                   require=False,
                                   default=None)
       word_count=forms.IntegerField(lebal='字数');
       chapter_count=forms.IntegerField(lebal='章节数')
       update_status=forms.ChoiceField('status',choices=[(1,"连载中"),(2,"已完结")],widget=forms.RadioSelect)
       source_id=forms.IntegerField(lebal='source id')
       source_url=forms.URLField('source url')
       '''
       title=forms.CharField(
                               label='标题',
                               min_length=1,
                               max_length=256,
                               error_messages={
                                               'required': '昵称不能为空！',
                                               'min_length':'标题不能为空！',
                                               'max_length': '不能超过256个字！'
                                               })
       content=forms.CharField(
                               label='内容摘要',
                               min_length=10,
                               max_length=1024,
                               error_messages={
                                               'required': '昵称不能为空！',
                                               'min_length':'不能少于10个字！',
                                               'max_length': '不能超过2000个字！'
                                               })
       class Meta:
           
           model=Document
           widgets = {
             'update_status': forms.Select(choices=((1,"连载中"),(2,"已完结")))     
            #'update_status': forms.ChoiceField(label='status',choices=(('1',"连载中"),('2',"已完结")),widget=forms.RadioSelect),
           }
    
      
            

        
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
            