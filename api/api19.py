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
PATTEN_FOR_ALT2=re.compile('alt=;P')
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

from cron.spider.spider import Category
class Lou19Category(Category):
    categoryDict = {
        u'都市/言情':104,
        u'言情小说':104,
        u'玄幻/奇幻':105,
        u'玄幻小说':105,
        u'穿越/重生':102,
        u'耽美/同人':107,
        u'武侠/仙侠':109,
        u'武侠小说':109,
        u'仙侠小说':110,
        u'网游小说':101,
        u'传奇小说':106,
        u'科幻小说':105,
        u'童话小说':106,
        u'恐怖小说':132,
        u'侦探小说':105,
        u'穿越':101,
        u'重生':102,
        u'都市':103,
        u'言情':104,
        u'玄幻':105,
        u'奇幻':106,
        u'耽美':107,
        u'同人':108,
        u'武侠':109,
        u'仙侠':110,
        u'末世':111,
        u'甜宠':112,
        u'女主':113,
        u'修仙':114,
        u'腹黑':115,
        u'空间':116,
        u'婚后':117,
        u'女强':118,
        u'女尊':119,
        u'现代':120,
        u'师徒':121,
        u'清穿':122,
        u'教授':123,
        u'帝王':124,
        u'架空':125,
        u'姐弟':126,
        u'小白':127,
        u'民国':128,
        u'修真':129,
        u'复仇':130,
        u'宫斗':131,
        u'黑道':132,
        u'总裁':133,
        u'婚恋':134,
        u'豪门':135,
        u'宠文':136,
        u'高干':137,
        u'肉文':138
    }

    def getCategoryByTags(self,tags):
        tagids=[]
        for tagName in tags:
            if self.categoryDict.has_key(tagName):
                cid = self.categoryDict[tagName]
                if not tagids.__contains__(cid):
                    tagids.append(cid)
        # if len(tagids)==0:
        #     tagids.append(2)
        return tagids #小说

    def getCategoryId(self,sourceCategoryName):
        if self.categoryDict.has_key(sourceCategoryName):
            cid = self.categoryDict[sourceCategoryName]
            return cid
        else:
            return 104


    # def getCategoryId(self,sourceCategoryId):
    #     return 104



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

    def getThreadPage(self,tid,page=1,default_tags=[]):
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
        tags=[]
        for tag in thread['tags']:
            tags.append(tag['name'])

        for key_tagname in Lou19Category.categoryDict.keys():
            if unicode(subject).__contains__(key_tagname):
                tags.append(key_tagname)

        forminfo = jsonContent["forum_info"]
        fid = int(forminfo["fid"])
        url= 'http://www.19lou.com/forum-%s-thread-%s-1-1.html'%(fid,tid)
        postList = jsonContent["post_list"]
        results=[]
        for post in postList:
            try:
                rawMessage=PATTEN_FOR_ALT.sub('"',post["message"]) #it's ugly
                rawMessage=PATTEN_FOR_ALT2.sub('/',rawMessage)
                message = self.stripTagsExcludeBr(rawMessage)
            except  HTMLParseError:
                message="错误！"
                logging.error(post['message'])
            title = post["subject"]
            titleString = self.stripTags(message[0:100])
            if len(title)==0:
                    ###获得回复得标题：取100字中，第一个标点符号前面的内容，如果没有直接截取最前的10个字
                    try:

                        lines = re.split(u'\n', message)
                        for line in lines:
                            if len(line)>1 and len(line.strip(' \r\n'))>1:
                                title=line
                                if len(title)>20:
                                    title=title[:20]
                                break

                        else:
                            title = ""
                    except Exception,e:
                        logging.error(e.message)

            attachments=[]
            if post.has_key('attachment'):
                for attachment in post['attachment']:
                    attachments.append(attachment['middle_url'])

            user=post['author']
            reply_uid=long(user['uid'])
            reply_created_at=datetime.strptime(post['created_at'],'%Y-%m-%d %H:%M:%S')
            reply=RelyItem(rid=long(post['pid']),
                           uid=reply_uid,
                           subject=title,
                           content=message,
                           is_chapter=(uid==reply_uid & len(message)>10),
                           created_at=reply_created_at,
                           is_first=post['first'],
                           attachments=attachments)

            results.append(reply)

        doc=DocItem(tid=tid,
                    uid=uid,
                    url=url,
                    subject=subject,
                    reply_count=replyCount,
                    view_count=viewCount,
                    content=results[0].content,
                    tags=tags,
                    fid=fid,
                    created_at=created_at,
                    last_reply_at=last_reply_at)
        if len(results[0].attachments)>0:
            doc.cover_img=results[0].attachments[0]


        return DocItemDetailPage(docItem=doc,page_number=pageNum,reply_list=results)

if __name__=='__main__':
    api=ThreadApi()
    result=api.getThreadPage('4891369839152366')
    print result


