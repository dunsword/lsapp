# coding=utf-8
from django.db import models
from django.utils import timezone

class Document(models.Model):
    author_name=models.CharField('author name',max_length=256,null=True,default=None)
    title=models.CharField('bookname',max_length=256)
    content=models.CharField('content',max_length=1024)
    created_at=models.DateTimeField('created time', default=timezone.now)
    read_count=models.IntegerField('read count',default=0)
    like_count=models.IntegerField('like count',default=0)
    reply_count=models.IntegerField('reply count',default=0)
    update_status=models.SmallIntegerField('status',default=0)
    categoryid=models.IntegerField('category id')


class Feed(models.Model):
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

class Category(models.Model):
    name=models.CharField('category name',max_length=100)
