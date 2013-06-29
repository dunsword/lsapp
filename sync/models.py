# coding=utf-8
from django.db import models
from base.models import BaseModel

# Create your models here.
# class TopicSyncLog(BaseModel):
#     source_tid=models.BigIntegerField()
#     topicid=models.IntegerField()
#     source_uid=models.BigIntegerField()
#
# class ReplySyncLog(BaseModel):
#     source_tid=models.BigIntegerField()
#     topicid=models.IntegerField()
#     source_pid=models.BigIntegerField()
#     reply_id=models.IntegerField()
#     source_uid=models.BigIntegerField()

class source_author(BaseModel):
    class Meta:
        index_together = [["uid", "site_id"],]
    uid=models.BigIntegerField(u'UID',db_index=True)
    username=models.CharField(u'用户名',max_length=100)
    desc=models.CharField(u'介绍',max_length=1000)
    site_id=models.IntegerField(u'来源网站id',db_index=True)
