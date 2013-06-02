# coding=utf-8
'''
Created on 2012-11-29

@author: DELL
'''

#req = sbs.api.ThreadRequest(tokenId=100, tokenSecret='accessTest7118jqq54113accessTest', accessToken='100|30709440|c72c0814e20b46a25189443bc02b9729')
from api.sbs.api import ThreadRequest

sbs.setDefaultAppInfo(100, 'accessTest7118jqq54113accessTest', 'qptest', 'forum', '0FAYr6o6')
accessToekn='100|30709440|c72c0814e20b46a25189443bc02b9729'

req=ThreadRequest(accessToekn)

resp=req.getThreadView('1601', '24001355367161510', 1, 30)
print resp
print resp['post_list'][0]['message']