# coding=utf-8
import re

import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")

import urllib
from sgmllib import SGMLParser


class WebPageContent:
    def __init__(self, url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()

    def getData(self):
        return self.htmlSource

    def writeData(self, fileContent, pid):
        fileName = "/tmp/%s.txt" % pid
        fSock = open(fileName, "wb")
        fSock.write(fileContent)
        fSock.close()


class BookInfoParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.updateTime = u''
        self.content = u''
        self.isUpdateTime = False
        self.isContent = False

    def handle_data(self, text):
        if self.isUpdateTime:
            self.updateTime = text.strip("\r\n").strip()

    def start_div(self, attrs):
        contentDiv = [v for k, v in attrs if k == 'id' and v == 'content']
        if contentDiv:
            self.isContent = True

    def end_div(self):
        if self.isContent:
            self.isContent = False

    def start_span(self, attrs):
        isUpdate = [v for k, v in attrs if k == 'id' and v == 'lblLastUpdateTime']
        if isUpdate:
            self.isUpdateTime = True

    def end_span(self):
        if self.isUpdateTime:
            self.isUpdateTime = False

    def start_script(self, attrs):
        if self.isContent:
            contentScript = [v for k, v in attrs if k == 'charset' and v == 'GB2312']
            if contentScript:
                try:
                    contentUrl = [v for k, v in attrs if k == 'src'][0]
                    if contentUrl:
                        c = WebPageContent(contentUrl)
                        self.content = c.getData().decode('GB2312').encode('utf-8').strip(u"document.write('").\
                            strip(u"<a href=http://www.qidian.com>起点中文网 www.qidian.com 欢迎广大书友光临阅读，"
                                  u"最新、最快、最火的连载作品尽在起点原创！</a>');").strip().replace(u'　',u'');
                except IndexError:
                    pass


class BookInfo:
    def __init__(self, url, pid = 0):
        self.url = url
        self.pid = pid
        self.run()

    def run(self):
        content = WebPageContent(self.url)
        parser = BookInfoParser()
        parser.feed(content.getData())
        parser.close()
        print parser.updateTime
        print parser.content
        #这里可以处理接下去的操作，发送内容
        # if self.pid:
        #     content.writeData(parser.content, self.pid)
        # else:
        #     print parser.updateTime
        #     print parser.content


if __name__ == "__main__":
    # BookList(2048120)
    BookInfo('http://read.qidian.com/BookReader/2517792,42152975.aspx')