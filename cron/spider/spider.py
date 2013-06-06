# coding=utf-8

import sys,urllib,logging

reload(sys)
sys.setdefaultencoding('utf-8')

class SpiderConfig:
    """
    提供基本的配置信息项
    """
    def __init__(self,httpDomain="127.0.0.1:8000",debug=True,logger=logging.getLogger()):
        self.httpDomain=httpDomain
        self.debug = debug
        self.logger = logger


class WebPageContent:
    """
    根据一个url获得页面内容，默认编码utf-8,如果有别的编码，需要转码，实现getData 方法。
    """
    def __init__(self, url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()

    def getData(self):
        """
        获得页面内容
        :return:
        """
        return self.htmlSource


class BookStore:
    """
    小说列表，包含小说的分类，及分类下的更新小说
    """
    bookStoreItem = []
    def __init__(self,category):
        self.category = category

    def appendBookItem(self,bookStoreItem):
        self.bookStoreItem.append(bookStoreItem)


class BookStoreItem:
    """
    小说列表包含内容：
    title  标题
    bookUrl 小说地址
    updateTime 最近更新时间
    latestCharpterUrl  最新章节地址
    """
    def __init__(self,title,bookUrl,latestCharpterUrl,updateTime):
        self.title=title
        self.bookUrl = bookUrl
        self.latestCharpterUrl = latestCharpterUrl
        self.updaeTime = updateTime



class Spider:
    spiderResult = []

    def __init__(self,spider,content):
        self.spiderImpl=spider
        self.analyzeContent = content

    def work(self):
        """
        爬虫处理数据
        :return:
        """
        pass

    def getData(self):
        return self.spiderResult

class DataStore:
    """
    爬虫数据处理,保存数据
    """
    def __init__(self,config):
        self.config = config

    def work(self,url,dataList,method="POST"):
        """
        发送数据请求到远端服务器
        :param url:
        :param data:
        :return:
        """
        pass

