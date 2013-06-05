# coding=utf-8
__author__ = 'paul'
from datetime import datetime


class RelyItem:
    '''
        回复信息对象
    '''
    def __init__(self,rid,uid,subject,content,is_chapter,is_first=False):
        self.rid=rid  #回复对象id，如pid
        self.uid=uid  #作者uid
        self.is_first=is_first
        self.is_chapter=is_chapter
        self.subject=subject
        self.content=content

class DocItem:
    '''
    列表中使用的文档摘要信息
    '''
    def __init__(self,tid,uid,subject,url,reply_count,view_count,content=None,fid=None,created_at=datetime.now(),updated_at=datetime.now()):
        self.tid=tid
        self.fid=fid  #板块id，如没有就不用
        self.content=content
        self.subject=subject
        self.url=url
        self.uid=uid
        self.reply_count=reply_count
        self.view_count=view_count
        self.created_at=created_at
        self.updated_at=updated_at
        self.siteid=0

class DocItemDetailPage():
    '''
        包含文档详细信息的对象，包含指定页面的回复信息列表
    '''
    def __init__(self,docItem,page_number,reply_list):
        self.docItem=docItem
        self.page_number=page_number
        self.reply_list=reply_list

class SourceInfo():
    def __init__(self,source_id,source_name,source_desc,site_id):
        self.source_id=source_id
        self.source_name=source_name
        self.source_desc=source_desc
        self.site_id=site_id

class DocumentList():
    def __init__(self,source_info,doc_list):
        self.source_info=source_info
        self.doc_list=doc_list

class DocumentFetcher():
    def getDocumentPage(self,tid,page=1):
        '''
            获取一个文章页的接口，根据每个站点实现
            返回DocItemDetailPage对象
        '''
        pass

    def getLatestDocumentList(self,sid,size):
        '''
            获取最新的文章列表接口
            返回DocumentList对象
        '''
        pass


class LouDocFetcherImpl(DocumentFetcher):
    def getDocumentPage(self,tid,page=1):
        from api19 import ThreadApi
        docPage= ThreadApi().getThreadPage(tid,page)
        docPage.docItem.siteid=19
        return docPage

    def getLatestDocumentList(self,sid,size):

        from huatan import Huatan
        return Huatan().getThreadList(sid,1,size)


LouDocFetcher=LouDocFetcherImpl()