# coding=utf-
from django.db import models

# Create your models here.
# 获得页面数据，分析记录

class SourceCategory(models.Model):
    name = models.CharField(max_length=256, null=False)
    url = models.CharField(max_length=500, null=False)
    parent_id = models.BigIntegerField()
    source_id = models.IntegerField()  #来源站点，起点＝1


class DocumentMapping(models.Model):
    document_id = models.BigIntegerField()   #数据导入后的document id
    source_docid = models.BigIntegerField()  #原站的document id
