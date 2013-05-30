# coding=utf-8
from django.db import models
from django.utils import timezone
from datetime import datetime
from base.storage.client import AvatarClient

class BaseModel(models.Model):
    STATUS=[(1,u"正常"),(2,u"删除"),(3,u"隐藏")]
    status=models.IntegerField(u'状态',choices=STATUS,default=1,db_index=True)
    created_at=models.DateTimeField(u'创建时间', default=datetime.now(),db_index=True)
    updated_at=models.DateTimeField(u'更新时间', default=datetime.now(),db_index=True)
    
    def setStatus(self,status):
        self.status=status
        self.save()
    
    def save(self, *args, **kwargs):
        self.updated_at=datetime.now()
        super(BaseModel,self).save(*args, **kwargs)
    
    class Meta:
        abstract=True

class SiteSource(BaseModel):
    name=models.CharField('site name',max_length=256)
    homepage=models.URLField('site home page')
    desc=models.CharField('description',max_length=2048)

class TopicManager(models.Manager):
    def create_topic(self,user,title,content,categoryid):
        topic=Topic(userid=user.id,
                    username=user.username,
                    title=title,
                    content=content,
                    categoryid=categoryid,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    topic_type=Topic.TOPIC_TYPE_NORMAL)
        
        topic.save()
        return topic
        
class Topic(BaseModel):
    def __init__(self, *args, **kwargs):
        super(Topic,self).__init__(*args, **kwargs)
        self.document=None
        self._avatar_url=None
        self.category=None
        self.chapters=None

        
    objects=TopicManager()
    TOPIC_TYPE_NORMAL=1
    TOPIC_TYPE_DOCUMENT=2
    TOPIC_TYPE_VIDEO=3
    TOPIC_TYPE_SHOP=4
    
    userid=models.IntegerField(u'用户ID',db_index=True)
    username=models.CharField(u'用户名',max_length=30)
    title=models.CharField(u'标题',max_length=255)
    content=models.TextField(u'内容',max_length=50000)
    categoryid=models.IntegerField(u'标签',default=104,db_index=True)
    like_count=models.IntegerField(u'喜欢数',default=0)
    read_count=models.IntegerField(u'阅读数',default=0)
    reply_count=models.IntegerField(u'回复数',default=0)
    last_reply_at=models.DateTimeField(u'最新回复', default=datetime.now(),db_index=True)

    topic_type=models.IntegerField(u'帖子类型',choices=[(1,"普通"),(2,"小说"),(3,"视频"),(4,"购物")],default=1,db_index=True)
    catid_parent=models.IntegerField(u'分类',default=2,db_index=True)
    catid1=models.IntegerField(u'标签',default=0)
    catid2=models.IntegerField(u'标签',default=0)

    def getChapters(self):
        if self.chapters == None:
            self.chapters = TopicReply.objects.getChapters(self.id)

        return self.chapters

    def getChapter(self,replyid):
        chapters=self.getChapters()
        for c in chapters:
            if c.id==replyid:
                return c
        return None


    def getAvatarUrl(self):
        if self._avatar_url==None:
            self._avatar_url=AvatarClient.url('a_250X250_'+str(self.userid)+'.jpg')
        return self._avatar_url
    
    def getCategory(self):
        if self.category != None:
            return self.category
        self.category=Category.objects.get(pk=self.categoryid);
        return self.category
    
    def isDocument(self):
        return self.topic_type==Topic.TOPIC_TYPE_DOCUMENT
    
    def getDocument(self):
        if self.document:
            return self.document
        if self.topic_type==2:
            self.document= Document.objects.get(topic__exact=self)
            self.document.topic=self
            return self.document
        return None
#    def save(self, *args, **kwargs): 
#        super(Topic, self).save(*args, **kwargs) 
    

class DocumentManager(models.Manager):
    def create_document(self,userid,username,title,content,source_id,source_url,categoryid,author_name='',source_updated_at=datetime.now()):
        topic=Topic(
                                   userid=userid,
                                   username=username,
                                   title=title,
                                   content=content,
                                   categoryid=categoryid,
                                   catid1=0,
                                   catid2=0,
                                   topic_type=Topic.TOPIC_TYPE_DOCUMENT)
        topic.save()
        doc=Document(source_id=source_id,source_url=source_url,topic=topic,author_name=author_name,source_updated_at=source_updated_at)
        doc.save()
        return doc
    
class Document(models.Model):
    objects=DocumentManager()
    author_name=models.CharField(u'作者',max_length=256,null=True,default=None)
    word_count=models.IntegerField('字数',default=0);
    chapter_count=models.IntegerField('章节数',default=0)
    update_status=models.SmallIntegerField('更新状态',choices=[(1,"连载中"),(2,"已完结")],default=1,db_index=True)
    source_id=models.IntegerField('源网站')
    source_url=models.URLField('源地址')
    source_tid=models.BigIntegerField('来源ID',default=0)
    topic=models.OneToOneField(Topic,related_name='ref+')
    source_updated_at=models.DateTimeField(u'原文章最后更新时间', default=datetime.now(),db_index=True)

    def getSiteSource(self):
        return SiteSource.objects.get(pk=self.source_id)

class Feed(BaseModel):
#    FEED_TYPE_RECOMMEND=1
#    FEED_TYPE_UPDATE=2
#    FEED_TYPE_CATEGORY_HOT=3
#    
#    type={
#          Feed.FEED_TYPE_RECOMMEND:'推荐',
#          Feed.FEED_TYPE_UPDATE:'更新',
#          Feed.FEED_TYPE_CATEGORY_HOT:'热门',
#          }
    
    userid=models.IntegerField('user id')
    username=models.CharField('user name',max_length=30)
    docid=models.IntegerField('doc id')
    feed_type=models.SmallIntegerField('feed type',default=1)

class CategoryManager(models.Manager):
    def getCategory(self,parent_id=0):
        '''
                        根据内容推荐标签，TODO性能优化
        '''
        if parent_id>0:
            cats=self.filter(parent_id=parent_id).filter(level__exact=2)
        else:
            cats=self.filter(level__exact=1)
        
        return cats
        
        
    
class Category(BaseModel):
    objects=CategoryManager()
    name=models.CharField('category name',max_length=100)
    parent_id=models.IntegerField('parent category',default=0)
    level=models.IntegerField('category level',default=1)
    topic_count=models.IntegerField('topic count',default=0)
    models.DateTimeField('updated time', default=datetime.now(),db_index=True,)
    
    def __init__(self, *args, **kwargs):
        super(Category,self).__init__( *args, **kwargs)
        self.parent=None
    
    def getParent(self):
        if self.parent:
            return self.parent
        else:
            self.parent=Category.objects.get(pk=self.parent_id)
            return self.parent
    
    def getTags(self):
        return self.name.split('/')
    
    def getDisplayName(self):
        if self.level==1:
            return self.name
        else:
            return self.name+self.getParent().name
    
    def getHotTopics(self,size=20):
        #目前只推荐小说
        if self.level==1:
            q=Topic.objects.filter(catid_parent__exact=self.id).filter(topic_type__exact=2).order_by('-read_count')[0:size]
                #q=Document.objects.select_related().filter(topic__catid_parent__exact=categoryid).order_by('topic.read_count')[:size]
        else:
                #q=Document.objects.select_related().filter(topic__categoryid__exact=categoryid).order_by('topic.read_count')[:size]
            q=Topic.objects.filter(categoryid__exact=self.id).filter(topic_type__exact=2).order_by('-read_count')[0:size]
            #q=q.filter(topic_type__exact=2)[:size]
        return q    

class TopicReplyManager(models.Manager):
    def getChapters(self,topicid):
        chapters=self.raw('select id,title from ls_topicreply where topicid=%s and is_chapter=true limit 1000',[topicid])
        l=list(chapters)
        for i in range(0,len(l)):
            c=l[i]
            c.url=self.getReplyUrl(topicid,c.id)
            if i>0:
                c.previous=l[i-1]
            if i<len(l)-1:
                c.next=l[i+1]
        return l

    def getReplyUrl(self,topicid,replyid):
        q=TopicReply.objects.raw('select id,count(id) as count from ls_topicreply where topicid=%s and id<%s',[topicid,replyid])
        beforeCount=list(q)[0].count
        page=beforeCount/TopicReply.PAGE_SIZE+1
        return u'/topic/%s/%s#%s'%(topicid,page,replyid)

class TopicReply(BaseModel):
    PAGE_SIZE=10

    def __init__(self, *args, **kwargs):
        super(TopicReply,self).__init__(*args, **kwargs)
        self._avatar_url=None
        self.topic=None


    objects=TopicReplyManager()

    userid=models.IntegerField('UID')
    username=models.CharField('用户名',max_length=30)
    topicid=models.IntegerField('主题ID',db_index=True)
    title=models.CharField('标题',max_length=255,default="",blank=True)
    content=models.TextField('内容',max_length=50000)
    is_chapter=models.BooleanField('章节',default=False)
    source_url=models.URLField('来源地址')

    def save(self, *args, **kwargs):
        self.updated_at=datetime.now()
        super(BaseModel,self).save(*args, **kwargs)
        #清空缓存
        if self.is_chapter==True:
            self.getTopic().chapters=None
    
    def getAvatarUrl(self):
        if self._avatar_url==None:
            self._avatar_url=AvatarClient.url('a_250X250_'+str(self.userid)+'.jpg')
        return self._avatar_url

    def getTopic(self):
        if self.topic==None:
            self.topic=Topic.objects.get(pk=self.topicid)
        return self.topic


    def getChapter(self):
        return self.getTopic().getChapter(self.id)



