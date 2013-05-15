# coding=utf-8
import sys
import os
import re
import urllib
import thread
import threading
import random
from sgmllib import SGMLParser
from httplib2 import Http
from django.utils import simplejson as json

reload(sys)
sys.setdefaultencoding('utf-8')

'''
功能：目前采用抓取分类，然后按照分类进行抓取3页，然后对每页的每个链接抓取对应的信息
运行：直接运行文件，Spider类进行多线程分发，按照每个分类，进行不同的页面抓取（这里分类采用七点的大分类）
      Timer是根据不同的分类进行调用RecursionPage抓取页面包
全局参数说明：
      localDomain：远程需要调用写入接口的域名
      categoryDict：红袖和本地的对应关系，有些起点有的本地没有，暂时不调用
      userMap：用户字典，形式为cid对应一个用户list
      dirFileName：七点的日志，说明跑过那些东西，下次跑的时候只需要修改就行了
'''