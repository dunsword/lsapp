# coding=utf-
from django.db import models

# 记录已经导入过的数据id，以及相应的分类数据

class CategoryManager(models.Manager):
    def create_category(self,name,url,parent_id=0,source_id=1):
        category = SourceCategory.objects.create(name=name.strip("\r\n").strip(),
                                                 url=url,parent_id=parent_id,source_id=source_id)
        category.save()
        return category

class SourceCategory(models.Model):
    objects = CategoryManager()
    name = models.CharField(max_length=256, null=False)
    url = models.CharField(max_length=500, null=False)
    parent_id = models.BigIntegerField()
    source_id = models.IntegerField()        #来源站点，起点＝1

    def isExist(self,name):
        category = SourceCategory.objects.filter(name=name.strip("\r\n").strip())
        if category:
            return True
        return False

    def saveOrReturn(self,name,url,parent_id=0,source_id=1):
        category = SourceCategory.objects.get(name=name,url=url)
        if category:
            return category
        else:
            category = SourceCategory.objects.create_category(name='test1',
                                                          url="http://sss",
                                                          parent_id=0,
                                                          source_id=1)
            return category



class DocumentMapping(models.Model):
    document_id = models.BigIntegerField()   #数据导入后的document id
    source_document_id = models.BigIntegerField()  #原站的document id
    source_id = models.IntegerField()        #来源站点，起点＝1

    def isExist(self,sourceDocumentId):
        obj = DocumentMapping.objects.get(source_document_id=sourceDocumentId)
        if obj:
            return True
        return False


