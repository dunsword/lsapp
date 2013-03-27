# coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from ls.models import Document, Topic


class DocumentTest(TestCase):
   
    def test_create_documen(self):
        doc = Document.objects.create_document(userid=1,
                                               username='user1',
                                               title="新小说", 
                                               content="新小说内容，很长很长",  
                                               source_id=1, 
                                               source_url="http://www.qidian.com/xxx.html",
                                               categoryid=1)
        self.assertTrue(doc.id>=1, "doc save failed")
        self.assertTrue(doc.topic.id>=1, 'topic save failed')
