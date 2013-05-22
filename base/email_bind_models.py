#coding=utf-8
__author__ = 'paul'

from django.db import models
from base.models import BaseModel
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
import hashlib


class EmailBindManager(models.Manager):
    def createEmailBindRecord(self,uid,email):
        str_now=str(datetime.now())
        hash_code=hashlib.md5(str_now+str(uid)+str(email)).hexdigest()
        log=EmailBindRecord()
        log.userid=uid
        log.email=email
        log.active_code=hash_code
        log.is_used=False
        log.save()
        return log


class EmailBindRecord(BaseModel):

    class Meta:
        app_label='base'
        managed=True

    objects=EmailBindManager()

    userid  = models.IntegerField(_(u'uid'),db_index=True)
    email = models.EmailField(_(u'邮箱地址'))
    active_code = models.EmailField(_(u'激活码'),max_length=128)
    is_used=models.BooleanField(_(u'是否已使用'),default=False)



