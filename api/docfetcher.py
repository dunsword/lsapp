# coding=utf-8
__author__ = 'paul'
from datetime import datetime

class RateItem:
    def __init__(self,rate_id,pid,tid,fid,uid,username,content,created_at):
        self.rate_id=rate_id
        self.pid=pid
        self.tid=tid
        self.fid=fid
        self.uid=uid
        self.username=username
        self.content=content
        self.created_at=created_at

class RelyItem:
    '''
        回复信息对象
    '''
    def __init__(self,rid,uid,subject,content,is_chapter,created_at=datetime.now(),is_first=False,user_name='',attachments=[], replyUrl=u''):
        self.rid=rid  #回复对象id，如pid
        self.uid=uid  #作者uid
        self.is_first=is_first
        self.is_chapter=is_chapter
        self.created_at=created_at
        self.subject=subject
        self.content=content
        self.user_name=user_name
        self.attachments=attachments
        self.reply_url = replyUrl
        self.rates=None

class DocItem:
    '''
    列表中使用的文档摘要信息
    '''
    def __init__(self,tid,uid,subject,url,reply_count=0,view_count=0,tags='',content=None,fid=None,created_at=datetime.now(),updated_at=datetime.now(),last_reply_at=datetime.now(),cover_img=None,siteid=0):
        self.tid = tid
        self.fid = fid  #板块id，如没有就不用
        self.content = content
        self.subject = subject
        self.url = url
        self.uid = uid
        self.reply_count = reply_count
        self.view_count = view_count
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_reply_at = last_reply_at
        self.tags = tags
        self.cover_img = cover_img
        self.siteid = siteid

class DocItemDetailPage():
    '''
        包含文档详细信息的对象，包含指定页面的回复信息列表
    '''
    def __init__(self,docItem,page_number,reply_list):
        self.docItem=docItem
        self.page_number=page_number
        self.reply_list=reply_list

class SourceInfo():
    def __init__(self,source_id,source_name,source_desc,site_id,tags=[]):
        self.source_id=source_id
        self.source_name=source_name
        self.source_desc=source_desc
        self.site_id=site_id
        self.tags=tags

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

    def getLatestDocuentList(self,size):
        """
        获得站点排行榜的文章列表
        返回DocumentList对象
        """
        pass

