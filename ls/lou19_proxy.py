# coding=utf-8
import logging
import sys
import re
import os
import urllib
import random
from sgmllib import SGMLParser
import urllib2
from httplib2 import Http
import json
import time

reload(sys)
sys.setdefaultencoding('utf-8')


def getDocumentCharpters(siteid,tid,authorUid=0,begin=1,end=10):
    """
    siteid 站点id
    tid    原站点内容的唯一id
    authorUid ！＝0 的情况：获得该作者的内容（不包括其他用户的评论）
    begin、 end 开始结束章节
    siteid ＋ tid 可以唯一确定一篇小说，根据组合id获得章节内容，如果该内容不存在，需要从原站获取相应的内容并保存下来。
    """



    pass
