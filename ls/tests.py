# coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from ls.models import Document, Topic


class DocumentTest(TestCase):
    def test_add_document(self):
        """tttt
        Tests that 1 + 1 always equals 2.
        """
        topic = Topic.objects.create(title="新小说", content="新小说内容，很长很长", userid=1, topic_type=Topic.TOPIC_TYPE_DOCUMENT)
        doc = Document.objects.create(source_id=1, source_url="http://www.qidian.com/xxx.html", topic=topic)
        doc.save()
        
        doc2 = Document.objects.get(pk=doc.id)
        self.assertIsNotNone(doc2, 'doc save failed')
        self.assertIsNotNone(doc2.topic, 'topic save failed')
        
    def test_create_documen(self):
        doc = Document.objects.create_document(userid=1,
                                               title="新小说", 
                                               content="新小说内容，很长很长",  
                                               source_id=1, 
                                               source_url="http://www.qidian.com/xxx.html",
                                               categoryid=1)
        self.assertTrue(doc.id>=1, "doc save failed")
        self.assertTrue(doc.topic.id>=1, 'topic save failed')
