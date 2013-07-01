# coding=utf-8

import sys,urllib,urllib2
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from datetime import datetime
from base.models import User3rdInfo,User

User3rdType_QQ = 1

@csrf_exempt
def qqAuthor(request):
    code =request.REQUEST.get("code")
    qq = QQAuthor()
    accessToken = qq.get_token(code)
    openid = qq.get_openid(accessToken)

    qqUserInfos = User3rdInfo.objects.filter(sid = openid,type=1)
    if qqUserInfos and qqUserInfos[0] :
        qqUserInfo =qqUserInfos[0]
        # user = User.objects.get(id = qqUserInfo.userid)
        user = authenticate(username=qqUserInfo.nick_name, password=openid)
        # user.username = qqUserInfo.nick_name
        login(request,user)
    else:
        userinfo = qq.get_userinfo(accessToken,openid)
        nickname = userinfo["nickname"]
        gender = userinfo["gender"]
        user = User.objects.create_user(username=nickname,email=nickname+u'@qq.com',password=openid,gender=gender)
        # user.save()
        time =datetime.now()
        # reg_ip = HttpResponse(request.META['REMOTE_ADDR'])
        qqUserInfo = User3rdInfo(userid=user.id,sid=openid,type=User3rdType_QQ,nick_name=nickname,reg_ip=0,status=0,verified=0,access_updated_at=time,created_at=time,updated_at=time,expires_in=time,re_expires_in=time)
        qqUserInfo.save()
        user = authenticate(username=nickname, password=openid)
        # user.username = qqUserInfo.nick_name
        login(request,user)

    response = HttpResponse()
    # response.write("<script language=javascript>window.opener.location.href=window.opener.location.href;window.close();</script>")
    response.write("<script language=javascript>window.opener.location.reload();window.close();</script>")
    return response

class QQAuthor:
    appid = 100474600
    appkey = u'89321b04df2263fce5db7aaa339b7553'
    # 从请求中获得qq返回的code，用于获得Access_token
    token_url = u'https://graph.qq.com/oauth2.0/token'
    redirect_url = u'mobile-proxy.weibols.com/oauthor/qzone'
    openid_url = u'https://graph.qq.com/oauth2.0/me'
    userinfo_url = u'https://graph.qq.com/user/get_user_info'

    def get_code(self, request):
        return request.REQUEST.get('code')

    def get_token(self, code):
        token_url = '%s?%s'%(self.token_url, urllib.urlencode({
                                    'grant_type': 'authorization_code',
                                    'client_id': self.appid,
                                    'client_secret': self.appkey,
                                    'code': code,
                                    'redirect_uri': self.redirect_url,
                                }))
        req = urllib2.Request(token_url)
        resp = urllib2.urlopen(req)
        content = resp.read()
        access_token = urllib2.urlparse.parse_qs(content).get('access_token', [''])[0]
        return access_token


    def get_openid(self, token):
        openid_url = '%s?%s'%(self.openid_url, urllib.urlencode({
                                    'access_token': token,
                                }))
        req = urllib2.Request(openid_url)
        resp = urllib2.urlopen(req)
        content = resp.read()
        content = content[content.find('(')+1:content.rfind(')')]
        data = json.loads(content)
        return data.get('openid')

    def get_userinfo(self, token,openid):
        userinfo_url = '%s?%s'%(self.userinfo_url, urllib.urlencode({
                                    'access_token': token,
                                    'oauth_consumer_key':self.appid,
                                    'openid':openid,
                                }))
        req = urllib2.Request(userinfo_url)
        resp = urllib2.urlopen(req)
        content = resp.read()
        data = json.loads(content)
        return {"nickname": data["nickname"],"gender": self.genderConvert(data["gender"])}

    def genderConvert(self,gender):
        if gender == u'男':
            return 1
        if gender == u'女':
            return 2
        return 3
