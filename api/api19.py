## coding=utf-8
import logging
import sys,os
from httplib2 import Http
import json
import time,re
from docfetcher import DocItemDetailPage,DocItem,RelyItem
import re
from datetime import datetime


PATTEN_FOR_ALT=re.compile('"alt=""')
from HTMLParser import HTMLParser,HTMLParseError
class HTMLStripper(HTMLParser):
    """
    去除所有得html标签
    """
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


class HTMLStripperExcludeBr(HTMLParser):
    """
    去除html标签，除了<br>
    """
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)

    def handle_starttag(self, tag, attrs):
        if tag =="br":
            self.fed.append("\r\n")

    def handle_endtag(self, tag):
        if tag=='div':
            self.fed.append('\r\n')

    def get_data(self):
        return ''.join(self.fed)

class Lou19Config:
    client_id = 100
    client_secret = u"accessTest7118jqq54113accessTest"
    lou19Url = "https://www.19lou.com/api/thread/getThreadView?client_id=%d&client_secret=%s&filterWater=true"%(client_id,client_secret)

    httpHeaders = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}

class ThreadApi():


    prePage = 30
    def stripTags(self,html):
        s = HTMLStripper()
        s.feed(html)
        return s.get_data()

    def stripTagsExcludeBr(self,html):
        s = HTMLStripperExcludeBr()
        s.feed(html)
        return s.get_data()

    def getThreadPage(self,tid,page=1):
        getAll = False
        pageNum = int(page)
        postTmp = []
        headers = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}
        hClient = Http()
        subject = ""
        viewCount = 0
        replyCount = 0
        fid = 0
        threadUrl = Lou19Config.lou19Url + "&tid=%s"%(str(tid))+"&page="+str(pageNum)+"&perPage="+str(self.prePage)
        resp, content = hClient.request(threadUrl,"GET",headers=headers)
        content = content.decode('gb18030').encode('utf8')
        jsonContent = json.loads(content)
        currentPage = int(jsonContent["page"])


        thread = jsonContent["thread_info"]

        created_at=datetime.strptime(thread['created_at'],'%Y-%m-%d %H:%M:%S')
        last_reply_at=datetime.strptime(thread['last_post']['created_at'],'%Y-%m-%d %H:%M:%S')
        subject  = thread["subject"]
        viewCount = int(thread["views"])
        replyCount = int(thread["replies"])
        uid=long(thread['author']['uid'])


        forminfo = jsonContent["forum_info"]
        fid = int(forminfo["fid"])
        url= 'http://www.19lou.com/forum-%s-thread-%s-1-1.html'%(fid,tid)
        postList = jsonContent["post_list"]
        results=[]
        for post in postList:
            try:
                rawMessage=PATTEN_FOR_ALT.sub('"',post["message"]) #it's ugly
                message = self.stripTagsExcludeBr(rawMessage)
            except  HTMLParseError:
                message="错误！"
                logging.error(post['message'])
            title = post["subject"]
            titleString = self.stripTags(message[0:100])
            if len(title)==0:
                    ###获得回复得标题：取100字中，第一个标点符号前面的内容，如果没有直接截取最前的10个字
                    try:

                        lines = re.split(u'\r\n', message)
                        for line in lines:
                            if len(line)>1:
                                title=line
                                if len(title)>20:
                                    title=title[:20]
                                break

                        else:
                            title = ""
                    except Exception,e:
                        logging.error(e.message)

            user=post['author']
            reply_uid=long(user['uid'])
            reply_created_at=datetime.strptime(post['created_at'],'%Y-%m-%d %H:%M:%S')
            reply=RelyItem(rid=long(post['pid']),uid=reply_uid,subject=title,content=message,is_chapter=(uid==reply_uid),created_at=reply_created_at,is_first=post['first'])

            results.append(reply)
        doc=DocItem(tid=tid,uid=uid,url=url,subject=subject,reply_count=replyCount,view_count=viewCount,content=results[0].content,fid=fid,
                    created_at=created_at,last_reply_at=last_reply_at)
        return DocItemDetailPage(docItem=doc,page_number=pageNum,reply_list=results)

if __name__=='__main__':
    api=ThreadApi()
    result=api.getThreadPage('4891369839152366')
    print result


