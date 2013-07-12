# coding=utf-8
__author__ = 'paul'

from httplib2 import Http
import json
import logging
import os
from time import sleep

LOG_FILENAME = os.path.dirname(__file__)+'/../../logs/sync.log'
FORMAT = logging.Formatter('%(asctime)-15s  %(message)s')

logger=logging.getLogger('sync')
handler=logging.FileHandler(LOG_FILENAME)
handler.setFormatter(FORMAT)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

#host='121.199.9.13'
host='127.0.0.1:8000'
def get_page(bid,page,type='board'):
    try:
        headers = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}
        hClient = Http()
        pageUrl = 'http://%s/sync/htsync/%d?page=%d&json=true&type=%s'%(host,bid,page,type)
        resp, content = hClient.request(pageUrl,"GET",headers=headers)
        jc = json.loads(content)
        if jc['result']=='success':
            return jc
    except Exception ,e :
        logger.error(u"获取第"+str(page)+u"页错误:\r\n"+unicode(e))

    return None

def get_doc_page(tid,page):
    try:
        headers = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}
        hClient = Http()
        pageUrl = 'http://%s/sync/htsync/t/%d/%d?json=true'%(host,tid,page)
        resp, content = hClient.request(pageUrl,"GET",headers=headers)
        jc = json.loads(content)
        if jc['result']=='success':
            return jc
    except Exception ,e :
        logger.error( u'文档'+str(tid)+u'获取第'+str(page)+u'页错误:'+unicode(e))

    return None

sync_doc_count=0
sync_status=1
def getHuatan(bid,startPage,pageCount,type='board'):
    global sync_doc_count
    global sync_status
    #logger.info('start sync board:'+str(bid))
    rg=range(startPage,pageCount+1)
    for pp in rg:
        if sync_status==2: #stop
            break

        logger.info( 'start get '+str(bid)+' page '+str(pp))
        jc=get_page(bid,pp,type)
        if jc!=None:
            count=len(jc['docs'])
            logger.info( u'花坛('+str(bid)+u')获取文档列表第'+str(pp)+u"页成功！共"+str(count)+u'个文档')
            for d in jc['docs']:
               if sync_status==2:
                   break
               tid=int(d['tid'])
               if int(d['fid'])!= 26:
                   logger.info(u'文档不是26板块，不同步')
                   continue
               dp1 = get_doc_page(tid,1)
               if dp1==None:
                   logger.error(u'同步文档'+str(tid)+u'失败:'+d['title'])
                   continue
               else:
                   if type=='user':
                       logger.info(u'当前达人('+str(bid)+u')第'+str(pp)+u'页。')
                   else:
                       logger.info(u'当前花坛('+str(bid)+u')第'+str(pp)+u'页。')
                   logger.info(u'开始同步文档'+str(tid)+u'，第1页同步成功。共'+ str(dp1['totalPage'])+u'页')

               if not dp1['need_update_reply']:
                   logger.info(u'文档已经为最新，不需要同步回复。')
                   continue
               if not dp1['is_doc']:
                   logger.info(u'改Topic不是文档，不需要同步。')
                   continue
               sync_repy_count=dp1['sync_reply_count']
               start_page=sync_repy_count/18
               if start_page<2:
                   start_page=2
               totalPage=int(dp1['totalPage'])
               logger.info(u'已经同步了了'+str(sync_repy_count)+u'项回复，从第'+str(start_page)+u'页开始同步！')
               for p in range(start_page,totalPage+1):

                   if sync_status==3: #pause
                        pausing=True
                        while pausing:
                            sleep(3)
                            if sync_status==1:
                                pausing=False


                   dp=get_doc_page(tid,p)
                   if dp==None:
                      logger.error( u'同步文档'+str(tid)+u'第'+str(p)+u'页失败。')
                   else:
                      logger.info( u'同步文档'+str(tid)+u'第'+str(p)+u'页成功。')
               sync_doc_count=sync_doc_count+1
               logger.info( u'成功同步了'+str(sync_doc_count)+u'个文档。')
               logger.info( u'_______________________________________')

if __name__=='__main__':
    import sys
    import threading

    if len(sys.argv)>1:
        bid=long(sys.argv[1])
    else:
        bid=697031974

    type=raw_input("type:")
    sid=long(raw_input('id:'))
    start=long(raw_input('start_page:'))
    page=long(raw_input('page_count:'))

    # if len(sys.argv)>2:
    #     getPageCount=sys.argv[2]
    # else:
    #     getPageCount=200
    t=threading.Thread(target=getHuatan,args=(sid,start,page,type))
    t.start()

    while True:
        cmd=raw_input("sync>")
        if cmd==u'pause':
            print 'pause ...'
            sync_status=3

        elif cmd==u'continue':
            print 'continue ...'
            sync_status=1

        elif cmd==u'quit':
            print 'quitting ...'
            sync_status=2
            t.join()
            break
