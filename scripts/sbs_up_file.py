# coding=utf-8
'''
Created on 2012-11-29

@author: DELL
'''
from api import sbs
from api.sbs.api import UpImageRequest

sbs.setDefaultAppInfo(100, 'accessTest7118jqq54113accessTest', 'qptest', 'forum', '0FAYr6o6')

upReq=UpImageRequest()
f=open('d:/123.jpg','rb')
resp=upReq.upload(10064388, f)
print resp