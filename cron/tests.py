"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")
from django.test import TestCase
from cron.models import DocumentMapping,SourceCategory

class CronTest(TestCase):
    def test_add_documentMapping(self):

        doc = DocumentMapping.objects.create(document_id=1, source_document_id=2540310,source_id=1)
        doc.save()
        self.assertTrue(doc.id>=1,"doc save ok")


    def test_isExist(self):
        doc = DocumentMapping.objects.create(document_id=1, source_document_id=2540310,source_id=1)
        doc.save()
        # doc = DocumentMapping.objects.get(source_document_id=2540310)

        doc =DocumentMapping().isExist(2540310)
        self.assertTrue(doc)

    def test_create_category(self):
        category = SourceCategory.objects.create_category(name='test1',
                                                          url="http://sss",
                                                          parent_id=0,
                                                          source_id=1)
        self.assertTrue(category.id>=1,"category is save ok ")

    def test_saveOrReturn(self):
        category1 = SourceCategory.objects.create_category(name='test1',
                                                          url="http://sss",
                                                          parent_id=0,
                                                          source_id=1)
        category2 = SourceCategory().saveOrReturn(name="test1",url="http://sss")

        self.assertTrue(category1.id==category2.id," ok")
