# coding=utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')



from sync.converter import DocumentConvert
from ls.models import Document,TopicReply
from sync.sync_page import sycnThreadList
from api.docfetcher import DocumentList,DocItem
from api.LouDocFetcherImpl import LouDocFetcher
fecther=LouDocFetcher
convert=DocumentConvert()




for p in range(1,100):
    sycnThreadList(p)


