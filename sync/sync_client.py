# coding=utf-8
__author__ = 'paul'

from httplib2 import Http
import json

def get_page(bid,page):
    try:
        headers = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}
        hClient = Http()
        pageUrl = 'http://121.199.9.13/sync/htsync/%d?page=%d&json=true'%(bid,page)
        resp, content = hClient.request(pageUrl,"GET",headers=headers)
        jc = json.loads(content)
        if jc['result']=='success':
            return jc
    except Exception ,e :
        print "获取第"+str(page)+"错误："
        print e

    return None

def get_doc_page(tid,page):
    try:
        headers = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}
        hClient = Http()
        pageUrl = 'http://121.199.9.13/sync/htsync/t/%d/%d?json=true'%(tid,page)
        resp, content = hClient.request(pageUrl,"GET",headers=headers)
        jc = json.loads(content)
        if jc['result']=='success':
            return jc
    except Exception ,e :
        print u'文档'+str(tid)+u'获取第'+str(page)+u'页错误'
        print e

    return None


if __name__=='__main__':
    sync_doc_count=0
    for page in range(1,300):
        jc=get_page(2124418905,page)
        if jc!=None:
            count=len(jc['docs'])
            print u'获取文档列表第'+str(page)+u"成功！共"+str(count)+u'个文档'
            for d in jc['docs']:
               tid=int(d['tid'])
               dp1 = get_doc_page(tid,1)
               if dp1==None:
                   print u'同步文档'+str(tid)+u'失败:'+d['title']
                   continue
               else:
                   print u'同步文档'+str(tid)+u'成功。共'+ str(dp1['totalPage'])+u'页'
               totalPage=int(dp1['totalPage'])
               p=2
               for p in range(2,totalPage+1):
                   dp=get_doc_page(tid,p)
                   if dp==None:
                      print u'同步文档'+str(tid)+u'第'+str(p)+u'页失败。'
                   else:
                      print u'同步文档'+str(tid)+u'第'+str(p)+u'页成功。'
               sync_doc_count=sync_doc_count+1
               print u'成功同步了'+str(sync_doc_count)+u'个文档。'
               print u'_______________________________________'