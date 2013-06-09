# coding=utf-8
from docfetcher import DocumentFetcher
from api19 import ThreadApi
from huatan import Huatan
from api19 import Lou19Category
#
class LouDocFetcherImpl(DocumentFetcher):
    def getDocumentPage(self,tid,page=1):
        docPage= ThreadApi().getThreadPage(tid,page)
        docPage.docItem.siteid=19
        return docPage

    def getLatestDocumentList(self,sid,size):
        return Huatan().getThreadList(sid,1,size)


LouDocFetcher=LouDocFetcherImpl()
LouCategory=Lou19Category()
