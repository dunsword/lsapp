# coding=utf-8

import urllib

class WebPageContent:
    """ 根据url获得页面的内容用于数据分析 """
    def __init__(self,url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()
    def getData(self):
        return self.htmlSource


if __name__ == "__main__":
    cotent = WebPageContent("http://www.qidian.com/rss.aspx")
    print cotent.getData()