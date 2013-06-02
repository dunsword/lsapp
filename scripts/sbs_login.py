# coding=utf-8
'''
Created on 2012-11-29

@author: DELL
'''

#oauth=sbs.api.OAuthRequest()
#result=oauth.auth(u'100',u'accessTest7118jqq54113accessTest',u'西门吹气',u'pass1234')
#print result.decode('gbk'),
from api.sbs.api import OAuthRequest

sbs.setDefaultAppInfo(100, 'accessTest7118jqq54113accessTest', 'qptest', 'forum', '0FAYr6o6')
# accessToekn:100|30709440|c72c0814e20b46a25189443bc02b9729

authReq=OAuthRequest()
f=open('d:/123.jpg','rb')
resp=authReq.auth( u'西门吹气', u'pass1234')
print resp['access_token'] # 100|30709440|c72c0814e20b46a25189443bc02b9729
print resp
