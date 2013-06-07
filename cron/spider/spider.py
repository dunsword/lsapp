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


class Category:
    """
    通过category的mapping 提供根据原站的id或者名称，获得推荐分类id，需要实现下面的两个接口.
    缺省返回104.
    """
    def getCategoryId(self,sourceCategoryName):
        return 104

    def getCategoryId(self,sourceCategoryId):
        return 104

class SpiderUrlConvert:
    """
    每个站点自己实现，根据一个tid（对应具体的一本书）或者pid（对应y个具体的章节），转换成站点特定的url。
    """
    def convertBookUrl(self,tid):
        """
        根据书的id，获得对应书籍的特定url，用于获得书籍的章节列表
        """
        pass


class Spider:
    def work(self,spider,content):
        pass

    def getData(self):
        pass


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

