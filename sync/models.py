# coding=utf-8
from django.db import models
from base.models import BaseModel

# Create your models here.
class TopicSyncLog(BaseModel):
    source_tid=models.BigIntegerField()
    topicid=models.IntegerField()
    source_uid=models.BigIntegerField()

class ReplySyncLog(BaseModel):
    source_tid=models.BigIntegerField()
    topicid=models.IntegerField()
    source_pid=models.BigIntegerField()
    reply_id=models.IntegerField()
    source_uid=models.BigIntegerField()