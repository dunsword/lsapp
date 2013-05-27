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



if __name__ == "__main__":
    # url = u"https://www.19lou.com/api/thread/getThreadView?client_id=100&client_secret=accessTest7118jqq54113accessTest&tid=12011369225965883&authorUid=31004258&filterWater=true&page=1&perPage=10"
    # sock = urllib.urlopen(url)
    # returnContent = sock.read()
    # sock.close()
    # print sock

    params = json.dumps({'client_id': 100, 'client_secret': 'accessTest7118jqq54113accessTest', 'tid': 12011369225965883,
                               'authorUid': 31004258,'filterWater': 'True',
                               'page': 1,'perPage': 10}
                        )

    # params1 = {'client_id': 100, 'client_secret': 'accessTest7118jqq54113accessTest', 'tid': 12011369225965883,'authorUid': 31004258,'filterWater': 'True','page': 1,'perPage': 10}


    headers = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}
    h = Http()

    resp, content = h.request("https://www.19lou.com/api/thread/getThreadView?client_id=100&client_secret=accessTest7118jqq54113accessTest&tid=12011369225965883&authorUid=31004258&filterWater=true&page=1&perPage=10", "GET",headers=headers)

    # resp, content = h.request("https://www.19lou.com/api/thread/getThreadView", "GET",body=urllib.urlencode(params, True),headers=headers)

    print resp
    print '==================='
    content = content.decode('gb18030').encode('utf8')

    jsonContent = json.loads(content)
    postList = jsonContent["post_list"]
    for item in postList:
        print '+++++++++++++++++++++++++++++'
        print item["message"]
        print '+++++++++++++++++++++++++++++'
    print content