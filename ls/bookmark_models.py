# coding=utf-8
__author__ = 'paul'
from django.utils.translation import ugettext_lazy as _
from django.db import models
from base.models import BaseModel


class BookMark(BaseModel):
    uid = models.IntegerField(_(u'用户UID'), db_index=True)
    tid = models.IntegerField(_(u'帖子TID'))
    rid = models.IntegerField(_(u'回复RID'),default=0)
    title1=  models.CharField(_(u'帖子标题'), max_length=255, blank=True)
    title2=  models.CharField(_(u'回复标题'), max_length=255, blank=True)