# coding=utf-8
__author__ = 'paul'
from httplib2 import Http
import json
from datetime import timedelta,datetime
import random
import logging
log=logging.getLogger('info')

def randstr():
    n=datetime.now()
    y=str(n.year)
    m=str(n.month)
    d=str(n.day)
    h=str(n.hour)
    min=str(n.minute)
    s=str(n.second)
    plus=str(random.randint(0,1000))
    ss=y+m+d+h+min+s+plus
    result=u''
    for c in ss:
        intc=int(c)
        result=result+unichr(97+intc)
    return result

class AuthResult:
    def __init__(self,access_token,refresh_token,auth_time,expires):
        self.access_token=access_token
        self.refresh_token=refresh_token
        self.auth_time=auth_time
        self.expires=expires
class UserInfo:
    def __init__(self,username,email,mobile,gender):
        self.username=username
        self.email=email
        self.mobile=mobile
        self.gender=gender

class Auth():
    client_id = 100
    client_secret = u"accessTest7118jqq54113accessTest"
    auth_url=u"https://www.19lou.com/oauth/token?grant_type=password&username=%s&password=%s&client_id=%s&client_secret=%s"
    def _getJsonResult(self,api_url):
        headers = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}
        hClient = Http()
        resp, content = hClient.request(api_url,"GET",headers=headers)
        content=content.decode('gb18030').encode('utf8')
        json_result = json.loads(content)
        return json_result

    def authenticate(self,username,password):

        auth_url = u"https://www.19lou.com/oauth/token?grant_type=password&username=%s&password=%s&client_id=%s&client_secret=%s"%(username,password,self.client_id,self.client_secret)


        try:
            json_result = self._getJsonResult(auth_url)

            if json_result.has_key('access_token'):
                auth_time=datetime.now()
                expires_in=int(json_result['expires_in'])
                expires_time=timedelta(seconds=expires_in)
                expires=auth_time+expires_time
                auth_result=AuthResult(access_token=json_result['access_token'],
                                   refresh_token=json_result['refresh_token'],
                                   auth_time=auth_time,
                                   expires=expires)
                return auth_result
        except Exception,e:
            log.error(e)

        return None

    def getUserInfo(self,access_token):
        userinfo_url=u'http://www.19lou.com/api/user/getCurrentUserInfo?access_token=%s'%(access_token)
        json_result=self._getJsonResult(userinfo_url)
        user=json_result['user']
        username=user['user_name']
        if user.has_key('email'):
            email=user['email']
        else:
            email=u'link_'+randstr()+u'@weibols.com'
        if user.has_key('mobile'):
            mobile=user['mobile']
        else:
            mobile=None
        gender=user['gender']
        userInfo=UserInfo(username=username,email=email,mobile=mobile,gender=gender)
        return userInfo

if __name__=='__main__':
     username=u'田伯光的刀'
     password=unicode(raw_input('password:'))
     auth=Auth()
     result=auth.authenticate(username,password)
     if result:
        print result.access_token
        print result.refresh_token
        print result.auth_time
        print result.expires

        userInfo=auth.getUserInfo(access_token=result.access_token)
        print userInfo.username
        print userInfo.email
        print userInfo.mobile
