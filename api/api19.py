## coding=utf-8
import logging
import sys,os
from httplib2 import Http
import json
import time,re

from HTMLParser import HTMLParser
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

class ThreadApi(Lou19Config):


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
        threadUrl = self.lou19Url + "&tid=%s"%(str(tid))+"&page="+str(pageNum)+"&perPage="+str(self.prePage)
        resp, content = hClient.request(threadUrl,"GET",headers=headers)
        content = content.decode('gb18030').encode('utf8')
        jsonContent = json.loads(content)
        currentPage = int(jsonContent["page"])

        thread = jsonContent["thread_info"]
        subject  = thread["subject"]
        viewCount = int(thread["views"])
        replyCount = int(thread["replies"])
        uid=long(thread['author']['uid'])


        forminfo = jsonContent["forum_info"]
        fid = int(forminfo["fid"])
        url= 'http://www.19lou.com/forum-%s-thread-%s-1-1.html'%(fid,tid)
        postList = jsonContent["post_list"]
        result=[]
        for post in postList:
            message = self.stripTagsExcludeBr(post["message"])
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
            if post['is_first']=='true':
                is_first=True
            else:
                is_first=False
            result.append({"msg":message,
                           "pid":int(post["pid"]),
                           'is_first':is_first,
                           "title":title,
                           'uid':long(user['uid'])
            })
        return {"subject":subject,
                "fid":fid,
                "tid":tid,
                'uid':uid,
                'url':url,
                "viewCount":viewCount,
                "replyCount":replyCount,
                'currentPage':currentPage,
                "posts":result}

if __name__=='__main__':
    api=ThreadApi()
    result=api.getThreadPage('4891369839152366')
    print result


