# coding=utf-8
import re
import sys
import os
import thread
import threading
from cron.spider.book import BookInfo

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")

import urllib
from sgmllib import SGMLParser

bookContent = []
nextUrl = u''

'''
    1   : 106   # 奇幻
    21  : 105   # 玄幻
    2   : 109   # 武侠
    22  : 110   # 仙侠
    4   : 103   # 都市
    15  : 104   # 青春 这个暂时先对应 言情
    5   : xxx   # 历史 这个没法对应
    6   : 120   # 军事  这个暂时先对应 现代
    7   :       # 游戏
    8   :       # 竞技
    9   : 105   # 科幻
    10  :       # 灵异
    12  : 108   # 同人
    14  :       # 图文
    31  :       # 文学
    41  :       # 女生
'''

categoryDict = {
    '1': 106, # 奇幻
    '21': 105, # 玄幻
    '2': 109, # 武侠
    '22': 110, # 仙侠
    '4': 103, # 都市
    '15': 104, # 青春 这个暂时先对应 言情
    #'5': xxx, # 历史 这个没法对应
    '6': 120, # 军事  这个暂时先对应 现代
    #'7': '', # 游戏
    #'8': '', # 竞技
    '9': 105, # 科幻
    #'10': '', # 灵异
    '12': 108, # 同人
    #'14': '', # 图文
    #'31': '', # 文学
    #'41': '', # 女生
}


class BookStoreData:
    def __init__(self):
        self.title = u""
        self.linkUrl = u""
        self.categoryUrl = u""
        self.categoryName = u""
        self.parentCategoryUrl = u""
        self.parentCategoryName = u""


class WebPageContent:
    def __init__(self, url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()

    def getData(self):
        return self.htmlSource

    def writeData(self, fileName):
        fileContent = ""
        fSock = open(fileName, "wb")
        fSock.write(fileContent)
        fSock.close()


class ContentParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.bookStoreData = None
        self.isContent = False
        self.isTitle = False
        self.isTitleSpan = False
        self.isTitleDiv = False
        self.isCategory = False
        self.isCategoryDiv = False
        self.isNextDiv = False
        self.hasPrevious = False
        self.hasNextUrl = False

    def handle_data(self, text):
        if self.isTitle:
            title = text.strip("\r\n").strip()
            self.bookStoreData.title = title
        if self.isCategory:
            if self.bookStoreData.parentCategoryName:
                self.bookStoreData.categoryName = text.strip("\r\n").strip()
            else:
                self.bookStoreData.parentCategoryName = text.strip("\r\n").strip()

    def start_div(self, attrs):
        contentDiv = [v for k, v in attrs if k == 'class' and v == 'swz']
        if contentDiv:
            self.bookStoreData = BookStoreData()
            bookContent.append(self.bookStoreData)
            self.isContent = True

        titleDiv = [v for k, v in attrs if k == 'class' and v == 'swb']
        if titleDiv:
            self.isTitleDiv = True

        catDiv = [v for k, v in attrs if k == 'class' and v == 'swa']
        if catDiv:
            self.isCategoryDiv = True

        if not nextUrl:
            nextUrlDiv = [v for k, v in attrs if k == 'class' and v == 'storelistbottom']
            if nextUrlDiv:
                self.isNextDiv = True

    def end_div(self):
        if self.isContent:
            self.isContent = False
        if self.isCategoryDiv:
            self.isCategoryDiv = False
        if self.isNextDiv:
            self.isNextDiv = False

    def start_span(self, attrs):
        if self.isTitleDiv:
            titleSpan = [v for k, v in attrs if k == 'class' and v == 'swbt']
            if titleSpan:
                self.isTitleSpan = True

    def end_span(self):
        if self.isTitleDiv:
            self.isTitleDiv = False

    def start_a(self, attrs):
        if self.isTitleSpan:
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
                self.isTitle = True
                self.bookStoreData.linkUrl = linkUrl
            except IndexError:
                pass
        if self.isCategoryDiv:
            try:
                catLink = [v for k, v in attrs if k == 'href'][0]
                self.isCategory = True
                if self.bookStoreData.parentCategoryUrl:
                    self.bookStoreData.categoryUrl = catLink
                else:
                    self.bookStoreData.parentCategoryUrl = catLink
            except IndexError:
                pass
        if self.isNextDiv:
            if self.hasPrevious:
                global nextUrl
                nextUrl = [v for k, v in attrs if k == 'href'][0]
                self.hasNextUrl = True
            if not self.hasPrevious:
                previousLink = [v for k, v in attrs if k == 'class' and v == 'f_s']
                if previousLink:
                    self.hasPrevious = True

    def end_a(self):
        if self.isTitleSpan:
            self.isTitleSpan = False
            self.isTitle = False
        if self.isCategory:
            self.isCategory = False
        if self.hasNextUrl:
            self.hasPrevious = False


class RecursionPage:
    def __init__(self, url, cid=0, startPage=1, totalPage=1):
        self.cid = cid
        self.url = url
        self.start = startPage
        self.end = totalPage
        self.run()

    def reset(self):
        del bookContent[0:len(bookContent)]
        global nextUrl
        nextUrl = u''

    def run(self):
        self.reset()
        content = WebPageContent(self.url)
        pattern = re.compile(r'http://.*?/')
        match = pattern.match(self.url)
        domain = ''
        if match:
            domain = match.group()
            domain = domain[0: int(len(domain)) - 1]
        parser = ContentParser()
        parser.feed(content.getData())
        parser.close()
        for item in bookContent:
            # print item.parentCategoryName
            # print item.parentCategoryUrl
            # print item.categoryName
            # print item.categoryUrl
            # print item.title
            # url = u''
            lMatch = pattern.match(item.linkUrl)
            if lMatch:
                url = item.linkUrl
            else:
                url = domain + item.linkUrl
            BookInfo(url, self.cid)
        if self.start < self.end:
            if nextUrl:
                RecursionPage(nextUrl, self.cid, self.start + 1, self.end)
        thread.exit_thread()


class timer(threading.Thread):
    def __init__(self, url, cid):
        threading.Thread.__init__(self)
        self.url = url
        self.cid = cid
        self.thread_stop = False

    def run(self):
        RecursionPage(self.url, self.cid)


class Sender():
    for key in categoryDict:
        url = u'http://all.qidian.com/Book/BookStore.aspx?ChannelId=%s' % key
        thread = timer(url, categoryDict[key])
        thread.start()


if __name__ == "__main__":
    Sender()
    # RecursionPage("http://all.qidian.com/book/bookstore.aspx")
    # RecursionPage("http://all.qidian.com/book/bookstore.aspx")