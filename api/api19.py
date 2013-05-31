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

    def get_data(self):
        return ''.join(self.fed)

class Lou19Config:
    client_id = 100
    client_secret = u"accessTest7118jqq54113accessTest"
    lou19Url = "https://www.19lou.com/api/thread/getThreadView?client_id=%d&client_secret=%s&filterWater=true"%(client_id,client_secret)

    httpHeaders = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}

class ThreadApi(Lou19Config):


    prePage = 50
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
        pageNum = 1
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
                        tmp = re.split(u'\,|\.|，|。', titleString)[0]
                        if tmp and len(tmp)>0:
                            title = tmp
                        else:
                            title = titleString[0:10]
                    except Exception,e:
                        logging.error(e.message)

            user=post['author']
            result.append({"msg":message,
                           "pid":int(post["pid"]),
                           "title":title,
                           'uid':int(user['uid'])
            })
        return {"subject":subject,
                "fid":fid,
                "tid":tid,
                'url':url,
                "viewCount":viewCount,
                "replyCount":replyCount,
                'currentPage':currentPage,
                "posts":result}

if __name__=='__main__':
    api=ThreadApi()
    result=api.getThreadPage('4891369839152366')
    print result


