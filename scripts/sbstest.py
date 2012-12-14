# coding=utf-8
'''
Created on 2012-11-29

@author: DELL
'''
import sbs.api

oauth=sbs.api.OAuthRequest()
result=oauth.auth(u'100',u'accessTest7118jqq54113accessTest',u'猪猪侠',u'pass123')
print result.decode('gbk'),


blist=sbs.api.BoardThreadListRequest()
r2=blist.getBoardThreadList(u'100', u'accessTest7118jqq54113accessTest', boardId='682585627')

boardThreadList=r2['board_thread_list']
print type(boardThreadList)

for thread in boardThreadList:
    print type(thread)
    print thread['fid']
    print thread['tid']
    print thread['board']['name']
    
    break