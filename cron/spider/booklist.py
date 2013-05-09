# coding=utf-8
import re

import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")

import urllib
from sgmllib import SGMLParser

bookList = []


class BookListData:
    def __init__(self):
        self.title = u""
        self.linkUrl = u""


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


class BookListParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.bookList = None
        self.isList = False
        self.isLink = False
        self.isContent = False

    def handle_data(self, text):
        if self.isLink:
            self.bookList.title = text.strip("\r\n").strip("' target='_blank'>").strip()

    def start_div(self, attrs):
        isContent = [v for k, v in attrs if k == 'id' and v == 'content']
        if isContent:
            self.isContent = True

        if self.isContent:
            isList = [v for k, v in attrs if k == 'class' and v == 'list']
            if isList:
                self.isList = True
            if self.isList:
                self.bookList = BookListData()
                bookList.append(self.bookList)

    def end_div(self):
        if self.isList:
            self.isList = False

    def start_a(self, attrs):
        if self.isList:
            self.isLink = True
            self.bookList = BookListData()
            bookList.append(self.bookList)
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
                self.bookList.linkUrl = linkUrl
            except IndexError:
                pass

    def end_a(self):
        if self.isLink:
            self.isLink = False

    def start_span(self,attrs):
        endContent = [v for k, v in attrs if k == 'id' and v == 'stxt']
        if endContent and self.isContent:
            self.isContent = False


class BookList:
    def __init__(self, fid):
        self.fid = fid
        self.url = u''
        self.pidPattern = re.compile(r'http://.*?/([a-zA-Z0-9,]+),([0-9]+)\.aspx')
        self.domain = u'http://read.qidian.com'
        self.run()

    def setUp(self):
        self.url = u'%s/BookReader/%d.aspx' % (self.domain, self.fid)

    def run(self):
        self.setUp()
        content = WebPageContent(self.url)
        pattern = re.compile(r'http://.*?/')
        parser = BookListParser()
        parser.feed(content.getData())
        parser.close()
        for item in bookList:
            if item.linkUrl and item.title:
                print item.title
                lMatch = pattern.match(item.linkUrl)
                if not lMatch:
                    item.linkUrl = self.domain + item.linkUrl
                print item.linkUrl
                m = self.pidPattern.match(item.linkUrl)
                if m:
                    print m.group(2)


if __name__ == "__main__":
    # BookList(2048120)
    BookList(2517792)