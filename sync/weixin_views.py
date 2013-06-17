# coding=utf-8
__author__ = 'paul'
import logging

from django.views.generic.base import View
import hashlib, time, re
from xml.etree import ElementTree as et
from django.http import HttpResponse
from django.shortcuts import render_to_response
log=logging.getLogger('info')
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from weixinapi import get_response
@csrf_exempt
def wexin(request):
    if request.method=='POST':
        log.log(logging.INFO,request.POST)
        xml = et.fromstring(request.raw_post_data)
        _rev= xml.find('Content').text
        _to = xml.find('FromUserName').text
        _from = xml.find('ToUserName').text
        _type = 'text'
        _resp = get_response(_rev,_to)

        if _resp['type']=='NEWS':
            return render_to_response('sync_weixin_tuwen.xml',{
                                        'to':_to,
                                        'from':_from,
                                        'time':int(time.time()),
                                        'type':'news',
                                        'docs':_resp['docs'],
                                    },
                                   mimetype='application/xml')



        # return render_to_response('sync_weixin.xml',
        #                           {'to':_to,
        #                            'from': _from,
        #                            'time' : int(time.time()),
        #                            'type': _type,
        #                            'content' : _content},
        #                           mimetype='application/xml')
    elif request.method=='GET':
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
        except Exception,e:
                return render_to_response('sync_weixin.html',{'echostr':''})
        return render_to_response('sync_weixin.html',{'echostr':''})

class WeixinView(View):
     def get(self,request,*args, **kwargs):
            log.log(logging.INFO,str(request.GET))
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
     @method_decorator(csrf_exempt)
     def post(self,request,*args, **kwargs):
            log.log(logging.INFO,request.raw_post_data)
            return render_to_response('sync_weixin.html',{'echostr':''})
