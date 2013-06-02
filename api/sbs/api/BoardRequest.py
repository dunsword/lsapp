'''
Created on 2012-12-10

@author: DELL
'''
import urllib
import json

from api.sbs.api import config

REQUEST_URL= config.SBS_API_URL+'board/getBoardThreadList'

class BoardThreadListRequest:
    
    def __init__(self):
        pass
    def getBoardThreadList(self,clientId,clientSecret,boardId,page=1,perPage=50):
        reqData={
                'bid':boardId,
                'page':page,
                'perPage':perPage,
                'client_id':clientId,
                'client_secret':clientSecret,
             }
        reqStr= config.dataToReqeustStr(reqData)
        f=urllib.urlopen(REQUEST_URL, reqStr)
        result=f.read()
        u_result = result.decode(config.SBS_API_ENCODE)
        jsonResult=json.loads(result, config.SBS_API_ENCODE)
        return jsonResult