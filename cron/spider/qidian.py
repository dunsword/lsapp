# coding=utf-8
__author__ = 'yanggz'

""" 根据特定的url获得具体的html内容，分析页面结构转化为结构化数据模型 """

import urllib
from sgmllib import SGMLParser
import feedparser

class WebPageContent:
    """ 根据url获得页面的内容用于数据分析 """
    def __init__(self,url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()
    def getData(self):
        return self.htmlSource


class ContentParser(SGMLParser):
    """ 内容解析，获得：标题、作者、内容介绍、总点击数、最后更新时间等 """
    def reset(self):
        SGMLParser.reset(self)
        self.intro = ""
        self.author = ""
        self.title = ""
        self.categoryUrls = []
        self.categoryName = []
        self.isBookInfo = False
        self.divCount = 0
        self.isTitle = False
        self.isTitleName = False
        self.isAuthor = False
        self.isIntro = False
        self.isIntroConten = False
        self.isNotProcess = False
        self.isCategory = False


    def start_a(self,attrs):
        if self.isCategory:
            href = [v for k, v in attrs if k == 'href']
            if href:
                self.categoryUrls.append(href)

    def start_div(self,attrs):
        """ 分析div 获得书籍的信息 """

        #获得小说所属分类的div
        categoryDiv = [v for k, v in attrs if k == 'class' and v == 'page_site']
        if categoryDiv:
            self.isCategory = True

        #获取小说的标题及简介div
        bookInfoDiv = [v for k, v in attrs if k == 'id' and v == 'divBookInfo']
        if bookInfoDiv:
            self.isBookInfo = True
        if self.isBookInfo:
            self.divCount += 1
        if self.isBookInfo:
            bookTitleDiv = [v for k, v in attrs if k == 'class' and v == 'title']
            if bookTitleDiv:
                self.isTitle = True
            introDiv = [v for k, v in attrs if k == 'id' and v == 'contentdiv']
            if introDiv:
                self.isIntro = True
            if self.isIntro:
                contentDiv = [v for k, v in attrs if k == 'class' and v == 'txt']
                if contentDiv:
                    self.isIntroConten = True

    def start_h1(self,attrs):
        if self.isTitle:
            self.isTitleName = True

    def end_h1(self):
        self.isTitleName = False
        self.isTitle = False


    def end_div(self):
        if self.isCategory:
            self.isCategory = False
        if self.isBookInfo:
            self.divCount -= 1
        if self.divCount == 0:
            self.isBookInfo = False

    def start_b(self,attrs):
        if self.isIntroConten:
            self.isNotProcess = True
    def end_b(self):
        if self.isIntroConten:
            self.isNotProcess = False

    def start_span(self,attrs):
        if self.isIntroConten:
            self.isNotProcess = True

    def end_span(self):
        if self.isIntroConten:
            self.isNotProcess = False
            self.isIntroConten = False

    def start_i(self,attris):
        if self.isCategory:
            self.isNotProcess = True

    def end_i(self):
        if self.isCategory:
            self.isNotProcess = False
            self.isCategory = False


    #处理各个html标签中的数据
    def handle_data(self, text):
        if self.isCategory and not self.isNotProcess:
            if str.strip(text) != ">" and len(str.strip(text)) > 0:
                self.categoryName.append(text.strip("\r\n"))
        if self.isTitle and self.isTitleName:
            self.title = text
        if self.isIntroConten and not self.isNotProcess and len(str.strip(text)) > 0:
            self.intro += text

    #以下获得提供的数据方法
    def getTitle(self):
        return self.title

    def getIntro(self):
        return self.intro

    def getCategoryUrls(self):
        return self.categoryUrls[1:len(self.categoryUrls) - 1]

    def getCategoryName(self):
        return self.categoryName[1:len(self.categoryName) - 1]

if __name__ == "__main__":

    # 获得起点的rss列表
    rss = feedparser.parse("http://www.qidian.com/rss.aspx")
    itemNum = len(rss.items())
    print "rss items num:%s" % (itemNum)

    rsslink = rss.entries[1].link
    print rsslink
    # myContent = WebPageContent("http://www.qidian.com/Book/2132495.aspx")
    myContent = WebPageContent(rsslink)
    parser = ContentParser()
    parser.feed(myContent.getData())
    parser.close()

    print parser.getTitle()

    print parser.getIntro()

    for url in parser.getCategoryUrls():
        print url
    for urlName in parser.getCategoryName():
        print urlName