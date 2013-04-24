# coding=utf-8
from django.db import models
from ls.models import BaseModel
from django.utils import timezone
from datetime import datetime
from base.storage.client import AvatarClient


class ReadRecord(BaseModel):
    userid=models.IntegerField('user id',db_index=True);
    topicid=models.IntegerField('topic id ')
    
    class Meta:
        app_label='ls'
        managed=True


class Feed(BaseModel):
    FEED_TYPE_CHOICES=[(1,"发帖"),(2,"阅读"),(3,"评分")]
    
    userid=models.IntegerField('user id',db_index=True);
    feed_type=models.SmallIntegerField('feed type',choices=Feed.FEED_TYPE_CHOICES,default=1,db_index=True)
    title=models.CharField('feet title',max_length=255)
    content=models.CharField('feed content',max_length=2048)
    class Meta:
        app_label='ls'
        managed=True

