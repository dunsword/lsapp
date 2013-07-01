# coding=utf-8
from django.views.generic.base import View
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect

class BaseView(View):
    def _get_json_respones(self,ctx, **httpresponse_kwargs):
        content= json.dumps(ctx);
        return HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)
        


class PageInfo(object): 
    class PageItem(object):
        def __init__(self,page,isCurrent):
            self.page=page
            self.isCurrent=isCurrent
        
    def __init__(self,page,itemCount,pageSize,baseUrl='./'):
        u'''
        :param page:当前页码
        :param itemCount: 总条目数
        :param pageSize: 每页显示条目数
        :param baseUrl: 页码数字前的链接地址
        '''
        self.baseUrl=baseUrl
        self.page=page
        self.itemCount=itemCount
        self.pageCount=self.getPageCount(itemCount, pageSize) #总页数
        self.items=self.getRange()
        self.startNum=(page-1)*pageSize
        self.endNum=self.startNum+pageSize
        
        #判断是否显示下一页
        if page<self.pageCount:
            self.next=page+1
        else:
            self.next=None
        
        #判断是否显示上一页
        if page>1:
            self.previous=page-1
        else:
            self.previous=None
        
        #判断是否显示第一页和最后一页
        self.first=None
        self.last=None
        small=page
        big=page
        for item in self.items:
            if small>item.page:
                small=item.page
            if big<item.page:
                big=item.page
        if small>1:
            self.first=1
        if big<self.pageCount:
            self.last=self.pageCount
            
    def getPageCount(self,itemCount,pageSize):
        pc =itemCount/pageSize
        if pc*pageSize < itemCount or pc==0:
            pc+=1
        return pc
    
    def getRange(self):
        start=self.getStart()
        end=start+4
        if end > self.pageCount:
            diff=end-self.pageCount
            end=self.pageCount
            start=start-diff
            if start<1:
                start=1
        return [PageInfo.PageItem(p,p==self.page) for p in range(start,end+1)]
        
    def getStart(self):
        start=self.page-2
        if start<1:
            start=1
        return start
        
