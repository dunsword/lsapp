# coding=utf-8
__author__ = 'paul'

from django.views.generic.base import View
import hashlib, time, re
from xml.etree import ElementTree as ET
from django.http import HttpResponse
from django.shortcuts import render_to_response

class WeixinView(View):

     def get(self,request,*args, **kwargs):
            try: # 微信接口认证 使用GET方式
                if request.method == 'GET':
                    token = 'weixinair2you'
                    tmpArr =[token, request.GET['timestamp'], request.GET['nonce']]
                    tmpArr.sort()
                    tmpArr.sort()
                    tmpStr = ''.join(tmpArr)
                    code = hashlib.sha1(tmpStr).hexdigest()
                    if code  == request.GET['signature']:
                        return HttpResponse(request.GET['echostr'])
                    else:
                        return HttpResponse('fail')
                # 微信接口通讯 返回用户需要数据
		        # elif request.method == 'POST':
                 #    pass
			        # xml = et.fromstring(request.raw_post_data)
			        # _to = xml.find('FromUserName').text
			        # _   from = xml.find('ToUserName').text
			        # _content = 'welcome!'
			        # _type = 'text'
			        # return render_to_response('air/weixin.xml',{'_to':_to, '_from': _from, '_time' : int(time.time()), '_type': _type, '_content' : _content}, mimetype='application/xml')
	            # else:
                 #    pass
            except Exception,e:
                return render_to_response('sync_weixin.html',{'echostr':''})
            return render_to_response('sync_weixin.html',{'echostr':''})

     def get1(self,request,*args, **kwargs):
            token = "dwmbnzjdqejltmndt"
            params = request.GET
            args = [token, params['timestamp'], params['nonce']]
            args.sort()
            if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
                if params.has_key('echostr'):
                     return HttpResponse(params['echostr'])

            return HttpResponse('failed')

