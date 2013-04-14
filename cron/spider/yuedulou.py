# coding=utf-8

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")

import urllib,random
from sgmllib import SGMLParser

class WebPageContent:
    """ 根据url获得页面的内容用于数据分析 """
    def __init__(self,url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()
    def getData(self):
        # print self.htmlSource.decode('gbk').encode('utf8')
        return self.htmlSource.decode('gb18030').encode('utf8')

threadContent = []

class ThreadData:
    def __init__(self):
        self.title = u""
        self.content = u""
        self.refUrl = u""
        self.readernum = []
        self.author = u""
        self.source = []
        self.catid = 0

class SpiderThread(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.threadData = None
        self.isContentDiv = False
        self.isTitle = False
        self.isContent = False
        self.getContent = False
        self.isTag = False
        self.isReadernum = False
        self.getReadernum = False
        self.getAuthor = False
        self.isAuthor  = False
        self.getSource = False

    def handle_data(self, text):
        if self.isContent and self.getContent:
            content = text.strip("\r\n").strip()
            if len(content)>0:
                self.threadData.content += text.strip("\r\n").strip()
                # print self.threadData.content
        if self.getReadernum:
            self.threadData.readernum.append(text.strip("\r\n").strip())
            # print "阅读数/回复数：" + text
        if self.getAuthor:
            self.threadData.author = text.strip("\r\n").strip()
            # print "==作者：%s"%(text.strip("\r\n").strip())
        if self.getSource:
            self.threadData.source.append(text.strip("\r\n").strip())

    def start_div(self,attrs):
        contentDiv = [v for k, v in attrs if k == 'class' and v == 'list-field']
        if contentDiv:
            self.isContentDiv = True
            self.threadData = ThreadData()
            # self.threadData.catid = self.catid
            threadContent.append(self.threadData)
        content = [v for k, v in attrs if k == 'class' and v == 'clearall list-con']
        if content:
            self.isContent = True
        #获得阅读数，回复数
        taginfo = [v for k, v in attrs if k == 'class' and v == 'clearall list-tags']
        if taginfo:
            self.isTag = True

        authorDiv = [v for k, v in attrs if k == 'class' and v == 'clearall list-source']
        if authorDiv:
            self.isAuthor = True



    def end_div(self):
        if self.isContent:
            self.isContent = False
        if self.isContentDiv:
            self.isContentDiv = False
        if self.isAuthor:
            self.isAuthor = False

    def start_h2(self,attrs):
        if self.isContentDiv:
            self.isTitle = True

    def end_h2(self):
        if self.isTitle:
            self.isTitle = False


    def start_a(self,attrs):
        if self.isTitle:
            self.threadData.refUrl = [v for k, v in attrs if k == 'href'][0]
            self.threadData.title = [v for k, v in attrs if k == 'title'][0].strip("\r\n").strip()
        if self.isAuthor:
            authorInfo = [v for k, v in attrs if k == 'class' and v == 'color']
            if authorInfo:
                self.getAuthor = True
            else:
                self.getSource = True

    def end_a(self):
        if self.getAuthor:
            self.getAuthor = False
        if self.getSource:
            self.getSource = False

    def start_span(self,attrs):
        if self.isContent:
            self.getContent = False
        if self.isTag:
            numberinfo = [v for k, v in attrs if k == 'class' and v == 'fr read']
            if numberinfo:
                self.isReadernum = True
        # if self.isAuthor:
        #     authorInfo = [v for k, v in attrs if k == 'class' and v == 'fl']
        #     if authorInfo:
        #         self.getAuthor = True


    def end_span(self):
        if self.isContent:
            self.getContent = True
        if self.isReadernum:
            self.isReadernum = False
            self.getReplynum = False
        # if self.isAuthor:
        #     self.isAuthor = False
        #     self.getAuthor = False

    def start_i(self,attrs):
        if self.isReadernum:
            self.getReadernum = True


    def end_i(self):
        if self.getReadernum:
            self.getReadernum = False


if __name__ == "__main__":
    from base.models import User
    from ls.models import Document,Category,Topic
    # url = "http://www.19lou.com/bq/都市%2F言情/dl-_s-_pg-1"
    # url = "http://www.19lou.com/bq/奇幻%2F玄幻/dl-_s-_pg-1"
    # http://www.19lou.com/board/rss/listRss?bid=2124418905&&page=3
    # catid1 = 108
    # catid2 = 0

    categorys = Category.objects.filter(level=2)
    urls = []
    threadIds = {}
    #
    for cat in categorys:
        i=1
        while i<3:
            # urls.append(("http://www.19lou.com/bq/%s小说/dl-_s-_pg-%s"%(cat.name.decode("utf8").encode("gbk"),i),cat.id))
            # urls.append(("http://www.19lou.com/bq/" + cat.name.decode("utf-8").encode("utf-8") + "小说/dl-_s-_pg-%s"%(i),cat.id))
            urls.append(("http://www.19lou.com/bq/" + cat.name.encode("utf-8") + "小说/dl-_s-_pg-%s"%(i),cat.id))
            i+=1

    urls.append(("http://www.19lou.com/bq/都市%2F言情/dl-_s-_pg-1",104))
    urls.append(("http://www.19lou.com/bq/都市%2F言情/dl-_s-_pg-2",104))
    for url in urls:
        threadContent = []
        print url[0]
        content = WebPageContent(url[0])
        parser = SpiderThread()
        catid = url[1]
        parser.feed(content.getData())
        parser.close()
         # print content.getData()
        for item in threadContent:
            if item.source[0]=="女性阅读":
                user = User.objects.get(id=random.randrange(5,450))
                if not item.refUrl in threadIds:
                        #新增加一个对象到DB
                    if user:
                        doc = Document.objects.create_document(userid=user.id,
                                                               username=user.username,
                                                               title=item.title,
                                                               content=item.content,
                                                               source_id=19,
                                                               source_url=item.refUrl,
                                                               categoryid=catid,
                                                                   # author_name='',
                                                               catid1=catid,
                                                               read_count=int(item.readernum[0]),
                                                               reply_count=int(item.readernum[1]))
                        threadIds[item.refUrl] = [1,doc.id]
                else:
                    threadId = threadIds[item.refUrl]
                    if threadId[0] == 1:
                        threadIds[item.refUrl] = [2,threadId[1]]
                            #帖子存在过，需要新修改个分类2
                        topic =  Document.objects.get(id=threadId[1]).topic
                        Topic.objects.filter(id=topic.id).update(catid2=catid)
                    else:
                            #已经更新过两次了，还是再新增加吧。
                        Document.objects.create_document(userid=user.id,
                                                         username=user.username,
                                                         title=item.title,
                                                         content=item.content,
                                                         source_id=19,
                                                         source_url=item.refUrl,
                                                         categoryid=catid,
                                                         # author_name='',
                                                         catid1=catid,
                                                         read_count=int(item.readernum[0]),
                                                         reply_count=int(item.readernum[1]))

                print item.title
                print "作者：" + item.author
                print item.content
                print item.refUrl
                print "阅读数：%s 回复数：%s"%(item.readernum[0],item.readernum[1])
                print item.source[0] + ">" + item.source[1]
        print
