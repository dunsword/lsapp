# coding=utf-8
import httplib2
from urllib import urlencode

h = httplib2.Http('.cache')
content='''
<xml><ToUserName><![CDATA[gh_54d09214e517]]></ToUserName>
<FromUserName><![CDATA[o5KjZjsK5fKg4JXITRQ7yg_uKzTs]]></FromUserName>
<CreateTime>1371093458</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[高跟鞋]]></Content>
<MsgId>5888801561969588536</MsgId>
</xml>
'''
response,content = h.request('http://127.0.0.1:8000/weixin',
                             'POST',
                             content,
                             headers={'Content-Type': 'application/x-www-form-urlencoded'})
print content