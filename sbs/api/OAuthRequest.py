'''
Created on 2012-11-29

@author: DELL
'''

import urllib
import config
from sbs.api.BaseRequest import BaseRequest 
OAUTH_URL='https://www.19lou.com/oauth/token'

class OAuthRequest(BaseRequest):

    def auth(self,username,password,scope=''):
        reqData={
                'grant_type':'password',
                'username':username,
                'password':password,
                'client_id':self.clientId,
                'client_secret':self.clientSecret,
                'scope':scope,
             }
       
        result=self.postReqData(OAUTH_URL, reqData)
        #data='grant_type=password&username='+qusername+'&password='+qpassword+'&client_id='+client_id.encode('gbk')+'&client_secret='+client_secret.encode('gbk')+'&scope='
        #print reqStr
#        f=urllib.urlopen(OAUTH_URL, reqStr)
#        result=f.read()
        return result