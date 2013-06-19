# coding=utf-8
from docfetcher import DocumentFetcher
from api19 import ThreadApi
from huatan import Huatan
from api19 import Lou19Category
#
class LouDocFetcherImpl(DocumentFetcher):
    def getDocumentPage(self,tid,page=1,tags=[]):
        docPage= ThreadApi().getThreadPage(tid,page,tags)
        docPage.docItem.siteid=19
        return docPage

    def getLatestDocumentList(self,sid,size,page=1,type='board'):
        if type=='board':
            return Huatan().getThreadList(sid,page,size)
        elif type=='forum':
            return Huatan().getForumThreadList(sid,page)


LouDocFetcher=LouDocFetcherImpl()
LouCategory=Lou19Category()
