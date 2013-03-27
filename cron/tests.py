"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from cron.models import DocumentMapping,SourceCategory

class CronTest(TestCase):
    def test_add_documentMapping(self):

        doc = DocumentMapping.objects.create(document_id=1, source_docid=2540310)
        doc.save()
        print "ok"
        # doc2 = Document.objects.get(pk=doc.id)
        # self.assertIsNotNone(doc2, 'doc save failed')
        # self.assertIsNotNone(doc2.topic, 'topic save failed')
