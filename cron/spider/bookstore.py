import re
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")

import urllib
from sgmllib import SGMLParser

bookContent = []


class BookStoreData:
    def __init__(self):
        self.title = u""
        self.linkUrl = u""
        self.categoryUrls = u""
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
        self.isTitle = False
        self.isTitleSpan = False
        self.isTitleDiv = False
        self.isCategory = False
        self.isParentCategory = False

    def handle_data(self, text):
        if self.isTitle:
            title = text.strip("\r\n").strip()
            self.bookStoreData.title = title
            # if self.isCategory:
            #     print text.strip("\r\n").strip()
            # if self.isParentCategory:
            #     print text.strip("\r\n").strip()

    def start_div(self, attrs):
        titleDiv = [v for k, v in attrs if k == 'class' and v == 'swb']
        if titleDiv:
            self.isTitleDiv = True
            self.bookStoreData = BookStoreData()
            bookContent.append(self.bookStoreData)

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

    def end_a(self):
        if self.isTitleSpan:
            self.isTitleSpan = False
            self.isTitle = False


if __name__ == "__main__":
    url = "http://all.qidian.com/Book/BookStore.aspx"
    content = WebPageContent(url)
    pattern = re.compile(r'http://.*?/')
    match = pattern.match(url)
    if match:
        domain = match.group()
        domain = domain[0: int(len(domain)) - 1]
    parser = ContentParser()
    parser.feed(content.getData())
    parser.close()
    for item in bookContent:
        print item.title
        lMatch = pattern.match(item.linkUrl)
        if lMatch:
            print item.linkUrl
        else:
            print domain + item.linkUrl