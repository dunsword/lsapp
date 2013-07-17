# coding=utf-8
from docfetcher import DocumentFetcher
from api19 import ThreadApi
from huatan import Huatan
from api19 import Lou19Category
from datetime import datetime
import logging
logger=logging.getLogger('perf')
#
class LouDocFetcherImpl(DocumentFetcher):
    def getDocumentPage(self,tid,page=1,tags=[]):
        st=datetime.now()
        docPage= ThreadApi().getThreadPage(tid,page,tags)
        logger.debug(u'获取帖子'+str(tid)+u'第'+str(page)+u'页用时：'+str((datetime.now()-st).total_seconds()))

        docPage.docItem.siteid=19
        return docPage

    def getLatestDocumentList(self,sid,size,page=1,type='board'):
        if type=='board':
            return Huatan().getThreadList(sid,page,size)
        elif type=='forum':
            return Huatan().getForumThreadList(sid,page)
        elif type=='user':
            return Huatan().getUserUserThreadList(sid,page)


LouDocFetcher=LouDocFetcherImpl()
LouCategory=Lou19Category()
